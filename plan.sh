pkg_name=threatstack-to-datadog
pkg_version=0.1.0
pkg_deps=(core/python2)
pkg_build_deps=(core/coreutils core/gcc core/python2)
pkg_origin=tmclaugh
pkg_maintainer='Tom McLaughlin'
pkg_expose=(8080)

# we copy in the source code in the `unpack` phase and need to put
# something here due to https://github.com/habitat-sh/habitat/issues/870
pkg_source="fake"

# Need to opt-out of all of these steps, as we're copying in source code
do_download() {
    return 0
}
do_verify() {
    return 0
}
do_clean() {
    return 0
}

do_unpack() {
    mkdir -p $pkg_prefix
    build_line "Copying ./ to $pkg_prefix/"
    cp -r $PLAN_CONTEXT/app $pkg_prefix/
    cp -r $PLAN_CONTEXT/*.py $pkg_prefix/
    cp -r $PLAN_CONTEXT/*.conf $pkg_prefix/
    cp -r $PLAN_CONTEXT/requirements.txt $pkg_prefix/
}

do_build() {
    pip install --upgrade pip
}

do_install() {
    cd $pkg_prefix
    pip install -r requirements.txt
    pip freeze
}


