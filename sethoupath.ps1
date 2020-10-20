# find houdini path
$hou_paths = Get-Childitem -Path 'C:\Program Files\Side Effects Software\'
$hou_dir = 'C:\Program Files\Side Effects Software\'+$hou_paths[0].name
$hou_path = ';'+$hou_dir+'\bin;'+ $hou_dir+'\custom\houdini\dsolib'
Write-Host "Use Houdini: "$hou_dir

# remove houdini related path in current PATH variable
$path_no_hou = [Environment]::GetEnvironmentVariable('Path', 'Machine').Split(";") | Where-Object { $_ -NotMatch "houdini" }
$path_no_hou = [string]::Join(";", $path_no_hou)

# set PATH variable
[Environment]::SetEnvironmentVariable(
    "Path",
    $path_no_hou + $hou_path,
    [EnvironmentVariableTarget]::Machine)