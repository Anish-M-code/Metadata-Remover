# Using Metadata-Remover Securely

Metadata-Remover Project uses external programs exiftool and ffmpeg for detecting and removing metadata, rest of the program is written
either in pure python or pure C , no other third party packages are used due to security reasons.

It is strongly advised to use Metadata-Remover only on Media you trust , incase if you have to process untrusted media it is strongly
recommended to use a sandbox or a dedicated virtual machine.

End users are requested to manually update exiftool.exe and ffmpeg.exe from https://exiftool.org and https://ffmpeg.org in case you
are using this program on windows operating system as these components bundled within this program maybe fairly outdated and lag behind security updates,
though we try our best to track security issues and provide security updates whenever possible.

## Reporting Security Issues

For all my personal projects in Github , i strongly believe in Full Public disclosure by making the details of security vulnerabilities public .
I feel Public scrutiny is the only reliable way to improve security, while secrecy only makes us less secure.

Like all other issues Feel free to open a Github Issue regarding the issue. 

Note: I cannot gurantee that all security problems brought to my attention will be fixed within a reasonable timeframe , as this is an personal
project but mostly such issues will be fixed as soon as possible.