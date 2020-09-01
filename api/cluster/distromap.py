"""This is a map that provides package information based on distro"""


def distro_map(distro=None, release=None,):
    if distro is 'ubuntu':
        if release is '18.04':
            init = 'systemd'
            packages = ['linux-image-kvm', 'grub-pc']
            return (init, packages)
