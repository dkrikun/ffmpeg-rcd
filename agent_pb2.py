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
  serialized_pb='\n\x0b\x61gent.proto\"\x86\x01\n\rFfmpegControl\x12%\n\x06opcode\x18\x01 \x01(\x0e\x32\x15.FfmpegControl.Opcode\"N\n\x06Opcode\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06RECORD\x10\x01\x12\x08\n\x04IDLE\x10\x02\x12\t\n\x05PAUSE\x10\x03\x12\x0b\n\x07UNPAUSE\x10\x04\x12\x0c\n\x08SHUTDOWN\x10\x05')



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
  serialized_start=72,
  serialized_end=150,
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
  serialized_end=150,
)

_FFMPEGCONTROL.fields_by_name['opcode'].enum_type = _FFMPEGCONTROL_OPCODE
_FFMPEGCONTROL_OPCODE.containing_type = _FFMPEGCONTROL;
DESCRIPTOR.message_types_by_name['FfmpegControl'] = _FFMPEGCONTROL

class FfmpegControl(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FFMPEGCONTROL

  # @@protoc_insertion_point(class_scope:FfmpegControl)


# @@protoc_insertion_point(module_scope)