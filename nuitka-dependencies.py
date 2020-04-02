# uncomment this if you need to package pygame
# import pygame
# import pygame.event
# import pygame.video
# import pygame.image
# import pygame.display
# import pygame

# external modules
import kivy.cache
import kivy.atlas
import kivy.network
import kivy.network.urlrequest
import kivy.lib.osc
import kivy.lib.osc.OSC
import kivy.lib.osc.oscAPI
import kivy.lib.mtdev
import kivy.lib.sdl2
import kivy.factory_registers
import kivy.input.recorder
import kivy.input.providers
import kivy.input.providers.tuio
import kivy.input.providers.mouse
import kivy.input.providers.wm_common
import kivy.input.providers.wm_touch
import kivy.input.providers.wm_pen
import kivy.input.providers.hidinput
import kivy.input.providers.linuxwacom
import kivy.input.providers.mactouch
import kivy.input.providers.mtdev

# compiled modules
import kivy.event
import kivy.graphics.buffer
import kivy.graphics.c_opengl_debug
import kivy.graphics.cgl_backend.cgl_glew
import kivy.graphics.cgl.cgl_get_backend_name
import kivy.graphics.cgl_backend.cgl_gl
import kivy.graphics.compiler
import kivy.graphics.context_instructions
import kivy.graphics.fbo
import kivy.graphics.instructions
import kivy.graphics.opengl
import kivy.graphics.opengl_utils
import kivy.graphics.shader
import kivy.graphics.stenctil_instructions
import kivy.graphics.texture
import kivy.graphics.transformation
import kivy.graphics.vbo
import kivy.graphics.vertex
import kivy.graphics.vertex_instructions
import kivy.graphics.tesselator
import kivy.graphics.svg
import kivy.graphics.cgl_backend
import kivy.properties

# core
# import kivy.core.audio.audio_gstplayer
# import kivy.core.audio.audio_pygst
# import kivy.core.audio.audio_sdl2
# import kivy.core.audio.audio_pygame
# import kivy.core.camera.camera_avfoundation
# import kivy.core.camera.camera_pygst
# import kivy.core.camera.camera_opencv
# import kivy.core.camera.camera_videocapture
# import kivy.core.clipboard.clipboard_sdl2
# import kivy.core.clipboard.clipboard_android
# import kivy.core.clipboard.clipboard_pygame
# import kivy.core.clipboard.clipboard_dummy
# import kivy.core.image.img_imageio
# import kivy.core.image.img_tex
# import kivy.core.image.img_dds
import kivy.core.image.img_sdl2
# import kivy.core.image.img_pygame
# import kivy.core.image.img_pil
# import kivy.core.image.img_gif
# import kivy.core.spelling.spelling_enchant
# import kivy.core.spelling.spelling_osxappkit
import kivy.core.text.text_sdl2
# import kivy.core.text.text_pygame
# import kivy.core.text.text_sdlttf
# import kivy.core.text.text_pil
# import kivy.core.video.video_gstplayer
# import kivy.core.video.video_pygst
# import kivy.core.video.video_ffmpeg
# import kivy.core.video.video_pyglet
# import kivy.core.video.video_null
import kivy.core.window.window_sdl2
import kivy.core.window.window_info
# import kivy.core.window.window_egl_rpi
# import kivy.core.window.window_pygame
# import kivy.core.window.window_sdl
# import kivy.core.window.window_x11
import kivy.uix.stacklayout
