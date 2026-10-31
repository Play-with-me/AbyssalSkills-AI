' SkillForge AI - Silent Launcher (Zero Terminal Window)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = currentDir

pythonwPath = currentDir & "\.venv\Scripts\pythonw.exe"
If fso.FileExists(pythonwPath) Then
    WshShell.Run Chr(34) & pythonwPath & Chr(34) & " main.py", 0, False
Else
    WshShell.Run "pythonw main.py", 0, False
End If
