buildarch="$(uname -m)"

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SPECS/ulyaoth-openssl1.1.0.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-openssl1.1.0.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-openssl1.1.0.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-openssl1.1.0.spec
fi

su ulyaoth -c "spectool ulyaoth-openssl1.1.0.spec -g -R"
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-openssl1.1.0.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-openssl1.1.0.sh
rm -rf /home/ulyaoth/rpmbuild