'''
Manage BSD packages and repositories. Note that BSD package names are case-sensitive.
'''

from pyinfra.api import operation

from .util.packaging import ensure_packages


@operation
def packages(state, host, packages=None, present=True, pkg_path=None):
    '''
    Install/remove/update pkg_* packages.

    + packages: list of packages to ensure
    + present: whether the packages should be installed
    + pkg_path: the PKG_PATH environment variable to set

    pkg_path:
        By default this is autogenerated as follows (tested/working for OpenBSD):
        ``http://ftp.<OS>.org/pub/<OS>/<VERSION>/packages/<ARCH>/``. Note that OpenBSD's
        official mirrors only hold the latest two versions packages.

        NetBSD/FreeBSD helpfully use their own directory structures, so the default won't
        work.
    '''

    if present is True:
        # Autogenerate package path
        if not pkg_path:
            host_os = host.fact.os or ''
            pkg_path = 'http://ftp.{http}.org/pub/{os}/{version}/packages/{arch}/'.format(
                http=host_os.lower(),
                os=host_os,
                version=host.fact.os_version,
                arch=host.fact.arch,
            )

    yield ensure_packages(
        packages, host.fact.pkg_packages, present,
        install_command='PKG_PATH={0} pkg_add'.format(pkg_path),
        uninstall_command='pkg_delete',
    )
