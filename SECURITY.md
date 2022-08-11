# Using Metadata-Remover Securely

Metadata-Remover Project uses external programs exiftool and ffmpeg for detecting and removing metadata, rest of the program is written
either in pure python or pure C , only mutagen and libmat2 from https://0xacab.org/jvoisin/mat2/ has been used for audio and torrent support in python version ,
no other third party packages were used due to security reasons.

It is strongly advised to use Metadata-Remover only on Media you trust , incase if you have to process untrusted media it is strongly
recommended to use a sandbox or a dedicated virtual machine.

End users are requested to manually update exiftool.exe and ffmpeg.exe from https://exiftool.org and https://ffmpeg.org in case you
are using this program on windows operating system as these components bundled within this program maybe fairly outdated and lag behind security updates,
though we try our best to track security issues and provide security updates whenever possible.

Note this program wont check online to see if newer versions of exiftool or ffmpeg or newer versions of this program itself is present.
It is the responsibilty of end user to check online and stay updated. No prompts will be provided by this program to update any component.

## Reporting Security Issues

For all my personal projects in Github , i strongly believe in Full Public disclosure by making the details of security vulnerabilities public .
I feel Public scrutiny is the only reliable way to improve security, while secrecy only makes us less secure.

Like all other issues Feel free to open a Github Issue regarding the issue. 

Note: I cannot gurantee that all security problems brought to my attention will be fixed within a reasonable timeframe , as this is an personal
project but mostly such issues will be fixed as soon as possible.
