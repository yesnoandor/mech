from ctypes import Structure, \
    POINTER, \
    c_bool, \
    c_ubyte, \
    c_short, \
    c_int, \
    c_longlong, \
    pointer, \
    byref


U8 = c_ubyte
U16 = c_short
U32 = c_int
U64 = c_longlong

CMD_CAN_TTX = 0x16      # Set ttx reference
CMD_CAN_TTX_CTL = 0x17  # enable/disable ttx reference, 0 disable, 1 enable


class ASET(Structure):
    _fields_ = [
        ('tseg1', U8),
        ('tseg2', U8),
        ('sjw', U8),
        ('smp', U8),
        ('brp', U16)
    ]


class DSET(Structure):
    _fields_ = [
        ('tseg1', U8),
        ('tseg2', U8),
        ('sjw', U8),
        ('smp', U8),
        ('brp', U16)
    ]


class ZCAN_FILTER(Structure):
    _fields_ = [
        ('type', U8),       # U8 type;      /**< 0-std_frame, 1-ext_frame */
        ('pad', U8 * 3),    # U8 pad[3];
        ('sid', U32),       # U32 sid;      /**< start-id */
        ('eid', U32),       # U32 eid;      /**< end-id */
    ]


class ZCAN_MSG_INF(Structure):
    _fields_ = [
        ('txm', U32, 4),    # U32 txm : 4;  /**< TX-mode, @see ZCAN_TX_MODE */
        ('fmt', U32, 4),    # U32 fmt : 4;  /**< 0-CAN2.0, 1-CANFD */
        ('sdf', U32, 1),    # U32 sdf : 1;  /**< 0-data_frame, 1-remote_frame */
        ('sef', U32, 1),    # U32 sef : 1;  /**< 0-std_frame, 1-ext_frame */
        ('err', U32, 1),    # U32 err : 1;  /**< error flag */
        ('brs', U32, 1),    # U32 brs : 1;  /**< bit-rate switch */
        ('est', U32, 1),    # U32 est : 1;  /**< error state */
        ('pad', U32, 19),   # U32 pad : 19;
    ]


class ZCAN_MSG_HDR(Structure):
    _fields_ = [
        ('ts', U32),                # /**< timestamp, 0.1ms */
        ('id', U32),                # /**< CAN-ID */
        ('inf', ZCAN_MSG_INF),      # /**< @see ZCAN_MSG_INF */
        ('pad', U16),
        ('chn', U8),                # /**< channel */
        ('len', U8)                 # /**< data length */
    ]


class ZCAN_INIT(Structure):
    _fields_ = [
        ('clk', U32),           # /**< clock(Hz) */
        ('mode', U32),          # /**< bit0-normal/listen_only, bit1-ISO/BOSCH */
        ('aset', ASET),
        ('dset', DSET)
    ]


class ZCAN_DEV_INF(Structure):
    _fields_ = [
        ('hmv', U16),       # /**< hardware version */
        ('fwv', U16),       # /**< firmware version */
        ('drv', U16),       # /**< driver version */
        ('api', U16),       # /**< API version */
        ('irq', U16),       # /**< IRQ */
        ('chn', U8),        # /**< channels */
        ('sn', U8*20),      # /**< serial number */
        ('id', U8*40),      # /**< card id */
        ('pad', U16*4),
    ]


class ZCAN_ERR_MSG(Structure):
    _fields_ = [
        ('hdr', ZCAN_MSG_HDR),
        ('dat', U8 * 8)
    ]


class CANFDMSG(Structure):
    _fields_ = [
        ('hdr', ZCAN_MSG_HDR),
        ('dat', U8 * 64)
    ]


class CAN20MSG(Structure):
    _fields_ = [
        ('hdr', ZCAN_MSG_HDR),
        ('dat', U8 * 8)
    ]


class ZCAN_STAT(Structure):
    _fields_ = [
        ('IR', U8),     # U8 IR;    /**< not used(for backward compatibility) */
        ('MOD', U8),    # U8 MOD;   /**< not used */
        ('SR', U8),     # U8 SR;    /**< not used */
        ('ALC', U8),    # U8 ALC;   /**< not used */
        ('ECC', U8),    # U8 ECC;   /**< not used */
        ('EWL', U8),    # U8 EWL;   /**< not used */
        ('RXE', U8),    # U8 RXE;   /**< RX errors */
        ('TXE', U8),    # U8 TXE;   /**< TX errors */
        ('PAD', U32),   # U32 PAD;
    ]


class ZCAN_TTX(Structure):
    _fields_ = [
        ('interval', U32), # 100 us
        ('repeat', U16), # repeat times, 0 for always
        ('index', U8), # TTX in the table, from 0 to 99
        ('flags', U8), # enable flag, 1 enable, 0 disable
        ('msg', CANFDMSG) # message body
    ]


class ZCAN_TTX_CFG(Structure):
    _fields_ = [
        ('size', U32), # The sizeof ZCAN_TTX array
        ('table', ZCAN_TTX * 8) # The arrry for ZCAN TTX
    ]
