# Using Metadata-Remover 

Metadata-Remover tool uses the external libraries exiftool and ffmpeg for detecting and removing the metadata. The rest of the program is written in Python or C. Only the modules mutagen and libmat2 from https://0xacab.org/jvoisin/mat2/ have been used for audio and torrent support in the Python version.
No other third party packages were used.

It is strongly advised to use Metadata-Remover only on data you trust. If the data is untrusted, use of a sandbox or virtual machine is 
recommended.

End users are expected to manually update exiftool.exe and ffmpeg.exe from https://exiftool.org and https://ffmpeg.org if using this program on Windows, as the components bundled with this program may be outdated and/or lag behind security updates.

This tool won't prompt the user at any moment to update its dependecies. It is the user's responsibility keeping those updated.

## Reporting Security Issues

For all my personal projects in Github, I strongly believe in full public disclosure by making the details of security vulnerabilities public.
I believe public scrutiny is the only reliable way to improve security, while secrecy only makes us more vulnerable.

Feel free to open a Github Issue if you find one. 

Note: I cannot guarantee that any issue brought up will be fixed in a reasonable timeframe. As this is a personal project, I will try my best to fix what I can.
