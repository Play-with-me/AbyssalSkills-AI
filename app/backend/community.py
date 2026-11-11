"""Real community catalog. Local legacy samples are never published automatically."""
import json
import hashlib
import uuid
import re
from .auth import AuthEngine
from .cloud_client import CloudClient, CloudError, failure
from .paths import get_data_dir, atomic_write, validate_skill_id
from .models import SkillItem


class CommunityService:
    @staticmethod
    def client(required=False):
        return CloudClient(token=AuthEngine.get_access_token(required=required))

    @staticmethod
    def normalize(item):
        return {**item, 'content': item.get('skill_content', ''),
                'author': item.get('author_name') or 'Community',
                'downloads': item.get('downloads_count', 0)}

    @classmethod
    def cache_file(cls, query, category, page):
        session = AuthEngine.public_session(AuthEngine._session)
        user_id = (session.get('user') or {}).get('id', 'anonymous')
        scope = [AuthEngine.get_config().get('supabase_url'), user_id, query, category, page]
        key = hashlib.sha256(json.dumps(scope, ensure_ascii=False).encode()).hexdigest()
        return get_data_dir() / 'community_cache' / (key + '.json')

    @classmethod
    def list_skills(cls, query='', category='', page=0):
        cache = cls.cache_file(query, category, page)
        try:
            client = cls.client()
            cache = cls.cache_file(query, category, page)
            response = client.rpc('list_community_skills', {'p_query': str(query)[:200], 'p_category': str(category)[:100], 'p_page': max(0, int(page))})
            response['skills'] = [cls.normalize(item) for item in response.get('skills', [])]
            result = {'success': True, 'status': 'success', 'source': 'cloud', **response}
            # A cache-write failure must not disguise a successful cloud response.
            try:
                atomic_write(cache, json.dumps(result, ensure_ascii=False))
            except OSError:
                result['cache_saved'] = False
            return result
        except (CloudError, OSError, ValueError) as error:
            try:
                saved = json.loads(cache.read_text(encoding='utf-8'))
                return {**saved, 'status': 'partial', 'source': 'cache', 'message': 'Đang xem bản đã lưu; chưa tải được cloud.'}
            except (OSError, ValueError):
                return {**failure(error), 'source': 'unavailable', 'skills': [], 'count': 0}

    @classmethod
    def publish(cls, data):
        try:
            slug = data.get('slug') or data.get('id') or ''
            validate_skill_id(slug)
            content = data.get('content') or data.get('skill_content') or ''
            if not content.strip():
                raise ValueError('Chưa có nội dung để đăng.')
            payload = {'slug': slug, 'id': data.get('cloud_id'), 'display_title': data.get('title') or data.get('display_title') or slug,
                       'description': data.get('description') or data.get('desc') or '',
                       'category': data.get('category') or 'Community', 'skill_content': content,
                       'version': data.get('version') or '1.0.0', 'tags': data.get('tags') or [],
                       'yaml_frontmatter': data.get('yaml_frontmatter') or {},
                       'references': data.get('references') or [], 'rules': data.get('rules') or []}
            # Reuse installer validation for reference/rule filenames before any network mutation.
            from .installer import SkillInstaller
            candidate = SkillItem.from_dict({**payload, 'id': slug, 'name': slug, 'references': payload['references'], 'rules': payload['rules']})
            SkillInstaller.skill_payload(candidate)
            payload['skill_content'] = candidate.skill_content
            payload['yaml_frontmatter'] = candidate.yaml_frontmatter
            row = cls.client(True).rpc('publish_skill', {'p_skill': payload})
            # Clear local community cache so this machine immediately gets fresh list
            try:
                cache_dir = get_data_dir() / 'community_cache'
                if cache_dir.exists():
                    for f in cache_dir.glob('*.json'):
                        try:
                            f.unlink(missing_ok=True)
                        except OSError:
                            pass
            except Exception:
                pass
            return {'success': True, 'status': 'success', 'skill': cls.normalize(row), 'skill_id': row['id'], 'message': 'Đã đăng công khai trên cloud.'}
        except (CloudError, OSError, ValueError, TypeError) as error:
            return failure(error)

    @classmethod
    def get_skill(cls, skill_id):
        row = cls.client().rpc('get_community_skill', {'p_id': skill_id})
        if not row:
            raise CloudError('Skill không tồn tại hoặc đã được gỡ.', 'NOT_FOUND', 404)
        return cls.normalize(row)

    @classmethod
    def action(cls, action, data):
        names = {'favorite': 'set_skill_favorite', 'remove': 'remove_community_skill',
                 'report': 'report_community_skill', 'moderate': 'moderate_community_skill',
                 'reports': 'list_community_reports'}
        try:
            result = cls.client(True).rpc(names[action], data)
            return {'success': True, 'status': 'success', 'result': result, 'message': 'Đã lưu thay đổi trên cloud.'}
        except (CloudError, OSError, ValueError, KeyError) as error:
            return failure(error)

    @classmethod
    def install(cls, data, workspace):
        from .installer import SkillInstaller
        from .models import InstallRequest
        from .storage import SkillStorage
        try:
            row = cls.get_skill(data['skill_id'])
            # Derive canonical folder slug: prefer slug or sanitized name
            raw_slug = row.get('slug') or row.get('name') or str(row['id'])
            canonical_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', raw_slug.lower()).strip('-')
            if not canonical_slug:
                canonical_slug = str(row['id'])
            item_dict = {
                **row,
                'id': canonical_slug,
                'name': row.get('slug') or row['name'],
                'skill_content': row['content'],
                'source_group': 'community',
                'cloud_id': str(row['id']),
            }
            item = SkillItem.from_dict(item_dict)
            force = bool(data.get('force_reinstall', False))
            result = SkillInstaller.install(
                item,
                InstallRequest(
                    item.id,
                    data.get('targets') or ['workspace'],
                    data.get('workspace_path') or workspace,
                    enable_always_on=True,
                    with_graphify=False,
                    overwrite=True,
                    force_reinstall=force
                )
            )
            if not result.success:
                return {'success': False, 'status': result.status, 'message': result.message, 'errors': result.errors, 'results': result.results}
            SkillStorage.upsert_skill(item)
            counted = True
            try:
                cls.client().rpc('record_skill_install', {'p_id': row['id'], 'p_request': str(uuid.uuid4())})
            except CloudError:
                counted = False
            return {'success': True, 'status': 'success', 'installed_paths': result.installed_paths,
                    'download_count_recorded': counted, 'message': 'Đã cài tệp skill từ cloud.' + ('' if counted else ' Chưa cập nhật được lượt cài trên cloud.')}
        except (CloudError, OSError, ValueError, KeyError) as error:
            return failure(error)
