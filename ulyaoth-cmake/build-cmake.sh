# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-cmake/SPECS/ulyaoth-cmake.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec

# Install additional requirements.
if type dnf 2>/dev/null
then
  sudo dnf builddep -y ulyaoth-cmake.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y ulyaoth-cmake.spec
fi

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec