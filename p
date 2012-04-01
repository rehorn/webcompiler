#!/bin/sh
cdnPWD='****'
webPWD='****'
cdnIp='*****'
webIp='*****'

echo 'compiling...'
python ../compiler/compile.py -f ./config.json nocompress
echo 'compile done.'
echo 'copy file to cdn...'
expect -c "set timeout 3600; \
            spawn rsync -e \"ssh -p36000 -o StrictHostKeyChecking=no\"  -rlpcgoDcv ./public/cdn/ root@$cdnIp:/***/; \
            expect *password* ;\
            send -- \"$cdnPWD\r\" ; \
            expect eof"
echo 'cdn done.'
echo 'copy file to module.qplus.com...'

expect -c "set timeout 3600; \
            spawn rsync -e \"ssh -p36000 -o StrictHostKeyChecking=no\"  -rlpcgoDcv ./public/webserver/ root@$webIp:/***/; \
            expect *password* ;\
            send -- \"$webPWD\r\" ; \
            expect eof"
echo 'webserver done.'
echo 'all done.'