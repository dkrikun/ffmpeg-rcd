# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='agent.proto',
  package='',
  serialized_pb='\n\x0b\x61gent.proto\"\xda\x02\n\rFfmpegControl\x12%\n\x06opcode\x18\x01 \x01(\x0e\x32\x15.FfmpegControl.Opcode\x12\x11\n\tcapture_x\x18\x06 \x01(\x05\x12\x11\n\tcapture_y\x18\x07 \x01(\x05\x12\x15\n\rcapture_width\x18\x08 \x01(\x05\x12\x16\n\x0e\x63\x61pture_height\x18\t \x01(\x05\x12\x13\n\x0b\x63\x61pture_fps\x18\n \x01(\x05\x12\x14\n\x0c\x61udio_device\x18\x0b \x01(\t\x12\x14\n\x0cvideo_device\x18\x0c \x01(\t\x12\x18\n\x10\x64\x65\x62ug_show_video\x18\r \x01(\x08\x12\x13\n\x0boutput_file\x18\x0e \x01(\t\x12\r\n\x05scale\x18\x0f \x01(\x01\"N\n\x06Opcode\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06RECORD\x10\x01\x12\x08\n\x04IDLE\x10\x02\x12\t\n\x05PAUSE\x10\x03\x12\x0b\n\x07UNPAUSE\x10\x04\x12\x0c\n\x08SHUTDOWN\x10\x05\"L\n\x0c\x46\x66mpegStatus\x12\x14\n\x0cis_recording\x18\x01 \x01(\x08\x12\x11\n\tis_paused\x18\x02 \x01(\x08\x12\x13\n\x0bhas_crashed\x18\x03 \x01(\x08')



_FFMPEGCONTROL_OPCODE = _descriptor.EnumDescriptor(
  name='Opcode',
  full_name='FfmpegControl.Opcode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECORD', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IDLE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNPAUSE', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHUTDOWN', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=284,
  serialized_end=362,
)


_FFMPEGCONTROL = _descriptor.Descriptor(
  name='FfmpegControl',
  full_name='FfmpegControl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opcode', full_name='FfmpegControl.opcode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_x', full_name='FfmpegControl.capture_x', index=1,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_y', full_name='FfmpegControl.capture_y', index=2,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_width', full_name='FfmpegControl.capture_width', index=3,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_height', full_name='FfmpegControl.capture_height', index=4,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_fps', full_name='FfmpegControl.capture_fps', index=5,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='audio_device', full_name='FfmpegControl.audio_device', index=6,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='video_device', full_name='FfmpegControl.video_device', index=7,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='debug_show_video', full_name='FfmpegControl.debug_show_video', index=8,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='output_file', full_name='FfmpegControl.output_file', index=9,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scale', full_name='FfmpegControl.scale', index=10,
      number=15, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FFMPEGCONTROL_OPCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=16,
  serialized_end=362,
)


_FFMPEGSTATUS = _descriptor.Descriptor(
  name='FfmpegStatus',
  full_name='FfmpegStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_recording', full_name='FfmpegStatus.is_recording', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_paused', full_name='FfmpegStatus.is_paused', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='has_crashed', full_name='FfmpegStatus.has_crashed', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=364,
  serialized_end=440,
)

_FFMPEGCONTROL.fields_by_name['opcode'].enum_type = _FFMPEGCONTROL_OPCODE
_FFMPEGCONTROL_OPCODE.containing_type = _FFMPEGCONTROL;
DESCRIPTOR.message_types_by_name['FfmpegControl'] = _FFMPEGCONTROL
DESCRIPTOR.message_types_by_name['FfmpegStatus'] = _FFMPEGSTATUS

class FfmpegControl(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FFMPEGCONTROL

  # @@protoc_insertion_point(class_scope:FfmpegControl)

class FfmpegStatus(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FFMPEGSTATUS

  # @@protoc_insertion_point(class_scope:FfmpegStatus)


# @@protoc_insertion_point(module_scope)
