LOCAL_PATH := $(call my-dir)
$(info build_androideabi_ffmpeg)
RESULT := $(shell PLATFORM_SDK_VERSION=$(PLATFORM_SDK_VERSION) $(LOCAL_PATH)/build_androideabi_ffmpeg.py)
$(info $(RESULT))
include $(LOCAL_PATH)/arm-linux-androideabi/Android.mk
