#!/bin/sh
cdnPWD='master@12345'
webPWD='pass4appstore'
cdnIp='10.133.0.234'
webIp='172.25.75.169'

echo 'compiling...'
python ../compiler/compile.py -f ./config.json nocompress
echo 'compile done.'
echo 'copy file to cdn...'
expect -c "set timeout 3600; \
            spawn rsync -e \"ssh -p36000 -o StrictHostKeyChecking=no\"  -rlpcgoDcv ./public/cdn/ root@$cdnIp:/data/qpluscdn/module/; \
            expect *password* ;\
            send -- \"$cdnPWD\r\" ; \
            expect eof"
echo 'cdn done.'
echo 'copy file to module.qplus.com...'

expect -c "set timeout 3600; \
            spawn rsync -e \"ssh -p36000 -o StrictHostKeyChecking=no\"  -rlpcgoDcv ./public/webserver/ root@$webIp:/data/sites/module.qplus.com/; \
            expect *password* ;\
            send -- \"$webPWD\r\" ; \
            expect eof"
echo 'webserver done.'
echo 'all done.'