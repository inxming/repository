ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

useradd ulyaoth

su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "cd /home/ulyaoth/rpmbuild/SPECS && wget https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SPECS/spotify-client.spec"

su ulyaoth -c "spectool /home/ulyaoth/rpmbuild/SPECS/spotify-client.spec -g -R"

if type dnf 2>/dev/null
then
  dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/spotify-client.spec
elif type yum 2>/dev/null
then
  yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/spotify-client.spec
fi

su ulyaoth -c "wget -O /home/ulyaoth/spotify-client_1.0.92.390.g2ce5ec7d-18_amd64.deb https://repository-origin.spotify.com/pool/non-free/s/spotify-client/spotify-client_1.0.92.390.g2ce5ec7d-18_amd64.deb"

su ulyaoth -c "cd /home/ulyaoth/ && ar x spotify-client_1.0.92.390.g2ce5ec7d-18_amd64.deb"
su ulyaoth -c "cd /home/ulyaoth/ && tar xvf data.tar.gz"

su ulyaoth -c "ln -s /usr/lib64/libcurl.so.4 /home/ulyaoth/usr/share/spotify/libcurl-gnutls.so.4"

su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/applications/"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/spotify.desktop /home/ulyaoth/usr/share/applications/"

su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/appdata/"
su ulyaoth -c "wget -O /home/ulyaoth/usr/share/appdata/spotify.appdata.xml https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SOURCES/spotify.appdata.xml"

su ulyaoth -c "mkdir -p /home/ulyaoth/usr/lib/firewalld/services/"
su ulyaoth -c "wget -O /home/ulyaoth/usr/lib/firewalld/services/spotify.xml https://raw.githubusercontent.com/ulyaoth/repository/master/spotify-client/SOURCES/spotify.xml"

su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/16x16/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/22x22/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/24x24/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/32x32/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/48x48/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/64x64/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/128x128/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/256x256/apps/"
su ulyaoth -c "mkdir -p /home/ulyaoth/usr/share/icons/hicolor/512x512/apps/"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-16.png /home/ulyaoth/usr/share/icons/hicolor/16x16/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-22.png /home/ulyaoth/usr/share/icons/hicolor/22x22/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-24.png /home/ulyaoth/usr/share/icons/hicolor/24x24/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-32.png /home/ulyaoth/usr/share/icons/hicolor/32x32/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-48.png /home/ulyaoth/usr/share/icons/hicolor/48x48/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-64.png /home/ulyaoth/usr/share/icons/hicolor/64x64/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-128.png /home/ulyaoth/usr/share/icons/hicolor/128x128/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-256.png /home/ulyaoth/usr/share/icons/hicolor/256x256/apps/spotify-client.png"
su ulyaoth -c "cp /home/ulyaoth/usr/share/spotify/icons/spotify-linux-512.png /home/ulyaoth/usr/share/icons/hicolor/512x512/apps/spotify-client.png"

su ulyaoth -c "cd /home/ulyaoth/ && tar cvf spotify-client.tar.gz ./usr/"
su ulyaoth -c "mv /home/ulyaoth/spotify-client.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"

su ulyaoth -c "rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/spotify-client.spec"

if [ "$os" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-spotify-client.sh