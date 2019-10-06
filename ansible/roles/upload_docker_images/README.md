# Uploading Docker Images

Ansilbe doesn't like transferring the large .tar files for some reason, so use sftp.

sftp root@new-node
cd ~/dockerimages
put *.tar
