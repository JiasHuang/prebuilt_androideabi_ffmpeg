#!/usr/bin/env python

import os
import re
import sys

def getEnv(name):
    if name in os.environ:
        return os.environ[name]
    else:
        print('%s not found' %(name))
        sys.exit()

def getSysroot():
    platform_sdk_version = int(getEnv('PLATFORM_SDK_VERSION'))
    for ver in range(platform_sdk_version, 0, -1):
        sysroot = getEnv('ANDROID_BUILD_TOP')+'/prebuilts/ndk/current/platforms/android-'+str(ver)+'/arch-arm/'
        if os.path.exists(sysroot):
            return sysroot
    print('sysroot not found')
    sys.exit()

def build_ffmpeg(prefix, cross_prefix, sysroot):

    cmd = '''
        ./configure \
        --enable-cross-compile \
        --target-os=linux \
        --arch=arm \
        --enable-shared \
        --disable-swresample \
        --disable-programs \
        --enable-small \
        --disable-static \
        --disable-doc \
        --disable-avdevice \
        --disable-swscale \
        --disable-postproc \
        --disable-avfilter \
        --disable-encoders \
        --disable-decoders \
        --disable-hwaccels \
        --disable-indevs \
        --disable-outdevs \
        --disable-filters \
        --disable-neon \
        --disable-symver \
        '''

    cmd += ' --prefix='+prefix
    cmd += ' --cross-prefix='+cross_prefix
    cmd += ' --sysroot='+sysroot

    cmd = re.sub(r'\s+', ' ', cmd)

    print(cmd)
    os.system(cmd)

    # remove version suffix
    os.system('sed -i \'s/SLIBNAME_WITH_VERSION=$(SLIBNAME).$(LIBVERSION)/SLIBNAME_WITH_VERSION=$(SLIBNAME)/g\' config.mak')
    os.system('sed -i \'s/SLIBNAME_WITH_MAJOR=$(SLIBNAME).$(LIBMAJOR)/SLIBNAME_WITH_MAJOR=$(SLIBNAME)/g\' config.mak')
    os.system('sed -i \'s/SLIB_INSTALL_NAME=$(SLIBNAME_WITH_VERSION)/SLIB_INSTALL_NAME=$(SLIBNAME)/g\' config.mak')
    os.system('sed -i \'s/SLIB_INSTALL_LINKS=$(SLIBNAME_WITH_MAJOR) $(SLIBNAME)/SLIB_INSTALL_LINKS=/g\' config.mak')

    os.system('make')
    os.system('make install')

def main():
    workdir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(workdir)
    if os.path.exists('arm-linux-androideabi/lib/libavcodec.so'):
        return
    if not os.path.exists('ffmpeg'):
        print('download ffmpeg')
        os.system('git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg')
    if not os.path.exists('ffmpeg/config.mak'):
        os.chdir('ffmpeg')
        print('compile ffmpeg')
        prefix = workdir+'/arm-linux-androideabi'
        cross_prefix = getEnv('ANDROID_TOOLCHAIN')+'/arm-linux-androideabi-'
        sysroot = getSysroot()
        build_ffmpeg(prefix, cross_prefix, sysroot)

if __name__ == "__main__":
    main()
