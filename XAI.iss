; 脚本头部信息
[Setup]
; 安装程序的名称，会显示在安装向导的标题栏等位置
AppName=XAI
; 应用程序的版本号
AppVersion=1.0.0
; 默认的安装目录，{pf} 代表系统的 Program Files 目录
DefaultDirName={pf}\My Application
; 安装程序生成的输出目录
OutputDir=output
; 安装程序的输出文件名
OutputBaseFilename=MyAppSetup
; 压缩方式，lzma 压缩率较高
Compression=lzma
; 是否进行固态压缩，可提高压缩率
SolidCompression=yes

; 要安装的文件信息
[Files]
; 将指定源文件夹中的所有文件添加到安装包中，复制到目标目录 {app}（即安装目录）
; recursesubdirs 表示递归复制子目录，createallsubdirs 表示创建所有必要的子目录
Source: "E:\AI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; 开始菜单快捷方式信息
[Icons]
; 在开始菜单组中创建一个名为 My Application 的快捷方式，指向安装目录下的可执行文件
Name: "{group}\My Application"; Filename: "{app}\xAI.exe"
; 可根据需要添加桌面快捷方式
Name: "{commondesktop}\My Application"; Filename: "{app}\main.exe"; Tasks: desktopicon

; 任务信息，用于控制是否创建桌面快捷方式
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; 安装完成后运行程序的设置
[Run]
; 安装完成后运行安装目录下的可执行文件
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,My Application}"; Flags: nowait postinstall skipifsilent