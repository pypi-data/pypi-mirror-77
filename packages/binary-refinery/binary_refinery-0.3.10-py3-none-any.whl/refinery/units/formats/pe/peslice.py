#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pefile

from .. import arg, MemoryExtractorUnit


class peslice(MemoryExtractorUnit):
    """
    Extract data from PE files based on virtual offsets.
    """

    def __init__(
        self, offset, count=0, utf16=False, ascii=False,
        base: arg.number('-b', help='Optionally specify a custom base address.') = 0
    ):
        self.superinit(super(), **vars())
        self.args.base = base

    def _get_file_offset(self, pe, offset):
        addr = offset.address
        end = None
        if offset.section:
            name = offset.section.encode('latin-1')
            for section in pe.sections:
                if section.Name.find(name) in (0, 1, 2):
                    addr += section.PointerToRawData
                    end = addr + section.SizeOfRawData
                    self.log_debug('found section', name, F'at offset 0x{addr:08X}')
                    break
            else:
                raise ValueError(F'section {offset.section} was not found.')
        else:
            base = self.args.base or pe.OPTIONAL_HEADER.ImageBase
            addr = pe.get_offset_from_rva(addr - base)
        return addr, end

    def process(self, data):
        try:
            pe = pefile.PE(data=data, fast_load=True)
        except Exception:
            raise ValueError('unable to parse input as PE file')

        return self._read_from_memory(data,
            lambda addr: self._get_file_offset(pe, addr))
