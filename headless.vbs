Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "path\to\program" & Chr(34), 0
Set WinScriptHost = Nothing
