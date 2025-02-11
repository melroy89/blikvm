#!/bin/bash
proc_name="kvmlink:master"
if [ -d "/usr/bin/blikvm" ]
then
    echo '/usr/bin/blikvm exists'
else
    mkdir -p "/usr/bin/blikvm"
fi

pid=$(ps -ef | grep "${proc_name}" | grep -v grep | awk '{print $2}')
if [ -n "${pid}" ]; then
  echo "Process $proc_name is running, killing it ..."
  kill -9 "${pid}"
fi

cp kvmd-web.sh /usr/bin/blikvm/kvmd-web.sh
chmod 777 /usr/bin/blikvm/kvmd-web.sh

cp kvm-link /usr/bin/blikvm/kvm-link
chmod 777 /usr/bin/blikvm/kvm-link

cp config.ini /usr/bin/blikvm/config.ini
chmod 777 /usr/bin/blikvm/config.ini

cp admin.ini /usr/bin/blikvm/admin.ini
chmod 777 /usr/bin/blikvm/config.ini

mkdir -p "/usr/lib/systemd/system"
cp kvmd-web.service "/usr/lib/systemd/system"

systemctl enable kvmd-web.service

echo "install web ok"