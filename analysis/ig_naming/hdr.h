
typedef unsigned long uintptr_t;

//arch types.h
typedef unsigned long long L4_Word64_t;
typedef unsigned long L4_Word32_t;
typedef unsigned short L4_Word16_t;
typedef unsigned char L4_Word8_t;

typedef unsigned long L4_Word_t;
typedef unsigned long L4_PtrSize_t;
typedef unsigned int L4_Size_t;

typedef short L4_Int16_t;
typedef L4_Word_t L4_SpaceId_t;
typedef L4_Word_t L4_Fpage_t;


// l4 types.h
typedef L4_Word_t L4_ThreadId_t;
typedef L4_Word_t L4_MsgTag_t;

// iguana types
typedef uintptr_t objref_t;
typedef objref_t memsection_ref_t;
typedef objref_t thread_ref_t;
typedef objref_t pd_ref_t;
typedef objref_t session_ref_t;
typedef objref_t eas_ref_t;
typedef objref_t hw_ref_t;
typedef objref_t quota_ref_t;
typedef objref_t pool_ref_t;
typedef objref_t physmem_ref_t;
typedef objref_t cap_t;

enum {INVALID_ADDR=0xffffffff};
enum {INVALID_CAP=0xffffffff};


// naming
struct naming_info;

struct notify {
    L4_ThreadId_t thread;
    uintptr_t mask;
    int flags;
    struct naming_info *naming_info;
};

struct notify_node {
    struct notify_node *next;
    struct notify_node *prev;
    struct notify data;
};

struct notify_list {
    struct notify_node *first;
    struct notify_node *last;
};

struct naming_info {
    uintptr_t data;
    /* list of notifications */
    struct notify_list notifies;
    char name[1];
};


typedef uintptr_t l4_threadid_t;
typedef l4_threadid_t CORBA_Object;
typedef struct {
  int _action;
  void *_data;
} idl4_server_environment;

int
naming_write_insert_impl(CORBA_Object _caller, objref_t nameserver, char *name,
                         objref_t data, uintptr_t *mask,
                         idl4_server_environment * _env);




// mutex
struct mutex {
    L4_Word_t holder;
    L4_Word_t needed;
    L4_Word_t count;
};

typedef struct mutex *mutex_t;

void mutex_init(mutex_t);
void mutex_lock(mutex_t);

void mutex_count_lock(mutex_t);
void mutex_count_unlock(mutex_t);

// malloc
struct header {
    struct header *ptr;
    unsigned size;
};


// stdio
struct __file {
    void *handle;

    size_t (*read_fn) (void *, long int, size_t, void *);
    size_t (*write_fn) (const void *, long int, size_t, void *);
    int (*close_fn) (void *);
    long int (*eof_fn) (void *);

    unsigned char buffering_mode;
    char *buffer;

    unsigned char unget_pos;
    long int current_pos;

    struct mutex mutex;

    int eof;
    int error;

    char unget_stack[10];
};

// iguana object.h
enum {
  IGUANA_GETENV_CLIST_SLOT=1,
  IGUANA_GETENV_CLIST_USED,
  IGUANA_GETENV_CLIST_BASE,
  IGUANA_GETENV_STACK      ,
  IGUANA_GETENV_HEAP_BASE  ,
  IGUANA_GETENV_HEAP_SIZE  ,
  IGUANA_GETENV_CALLBACK   ,
  IGUANA_GETENV_DEFAULT_POOL ,
  IGUANA_GETENV_DEFAULT_VIRT_POOL ,
  IGUANA_GETENV_TCM_POOL,
};

enum {
  IGUANA_GETENV_TIMER_SERVER=259,
  IGUANA_GETENV_NAMING_SERVER=256,
  IGUANA_GETENV_TRACE_SERVER=257,
};

typedef struct {
    objref_t obj;
    L4_ThreadId_t server;
    struct session *session;
    struct cb_alloc_handle *call_cb;
    struct cb_alloc_handle *return_cb;
} object_t;

// cap.h
struct clist;
struct cap_slot {
    struct clist *list;
    int pos;
};

// kcp.h
typedef struct L4_KernelRootServer {
    L4_Word_t sp;
    L4_Word_t ip;
    L4_Word_t low;
    L4_Word_t high;
} L4_KernelRootServer_t;

typedef struct L4_KernelConfigurationPage {
    L4_Word_t magic;

    /* 0x04 */
    L4_Word_t __padding04;
    L4_Word_t __padding08;
    L4_Word_t __padding12;

    L4_KernelRootServer_t Kdebug;
    L4_KernelRootServer_t reserved0;
    L4_KernelRootServer_t reserved1;
    L4_KernelRootServer_t root_server;

    /* 0x50 */
    L4_Word_t MaxMemoryDescs;

    L4_Word_t MemoryInfo;

    L4_Word_t Kdebug_config[2];

    /* 0x60 */
    L4_Word_t __padding60[16];

    /* 0xA0 */
    L4_Word_t __paddingA0[6];

    /* 0xB8 */
    L4_Word_t BootInfo;

    /* 0xBC */
    L4_Word_t __paddingBC[1];
} L4_KernelConfigurationPage_t;

enum  {
  KDB_FEATURE_CLI = 1,
  KDB_FEATURE_CONSOLE = 2,
  KDB_FEATURE_THREADNAMES = 0x100,
};



// vregs.h
enum trapenum {
L4_TRAP_KPUTC           = 0xffffffa0,
L4_TRAP_KGETC           = 0xffffffa4,
L4_TRAP_KGETC_NB        = 0xffffffa8,
L4_TRAP_KDEBUG          = 0xffffffac,
L4_TRAP_GETUTCB         = 0xffffffb0,
L4_TRAP_KIP             = 0xffffffb4,
L4_TRAP_KSET_THRD_NAME  = 0xffffffb8,
L4_TRAP_GETCOUNTER      = 0xffffffbc,
L4_TRAP_GETNUMTPS       = 0xffffffc0,
L4_TRAP_GETTPNAME       = 0xffffffc4,
L4_TRAP_TCCTRL          = 0xffffffc8,

L4_TRAP_PMU_RESET       = 0xffffffcc,
L4_TRAP_PMU_STOP        = 0xffffffd0,
L4_TRAP_PMU_READ        = 0xffffffd4,
L4_TRAP_PMU_CONFIG      = 0xffffffd8,

L4_TRAP_GETTICK         = 0xffffffe0,

USER_UTCB_REF           = 0xff000ff0,
};

enum tlsenum {
__L4_TCR_PLATFORM_OFFSET                = 48   ,

__L4_TCR_MR_OFFSET                      = 16,

__L4_TCR_IDL4_RESTORE_COUNT             = 15,
__L4_TCR_KERNEL_RESERVED4               = 15   ,

__L4_TCR_KERNEL_RESERVED3               = 14,
__L4_TCR_KERNEL_RESERVED2               = 13,
__L4_TCR_KERNEL_RESERVED1               = 12,
__L4_TCR_KERNEL_RESERVED0               = 11,

__L4_TCR_PREEMPTED_IP                   = 10,
__L4_TCR_PREEMPT_CALLBACK_IP            = 9,
__L4_TCR_VIRTUAL_ACTUAL_SENDER          = 8,
__L4_TCR_ERROR_CODE                     = 7,
__L4_TCR_PROCESSOR_NO                   = 6,
__L4_TCR_NOTIFY_BITS                    = 5,
__L4_TCR_NOTIFY_MASK                    = 4,

__L4_TCR_ACCEPTOR                       = 3,
__L4_TCR_COP_FLAGS                      = 2,
__L4_TCR_PREEMPT_FLAGS                  = 2,

__L4_TCR_USER_DEFINED_HANDLE            = 1,
__L4_TCR_MY_GLOBAL_ID                   = 0,
};

// tcr preempt values times four
enum tcr4enum {
x4TCR_PREEMPTED_IP                   = 40,
x4TCR_PREEMPT_CALLBACK_IP            = 36,
x4TCR_VIRTUAL_ACTUAL_SENDER          = 32,
x4TCR_ERROR_CODE                     = 28,
x4TCR_PROCESSOR_NO                   = 24,
x4TCR_NOTIFY_BITS                    = 20,
x4TCR_NOTIFY_MASK                    = 16,

x4TCR_ACCEPTOR                       = 12,
x4TCR_COP_FLAGS                      = 8,
x4TCR_PREEMPT_FLAGS                  = 8,

x4TCR_USER_DEFINED_HANDLE            = 4,
x4TCR_MY_GLOBAL_ID                   = 0,
};

enum tcr4enum2 {
x4TCR_PLATFORM_OFFSET                = 0xc0,
x4TCR_MR_OFFSET                      = 0x40,
x4TCR_IDL4_RESTORE_COUNT             = 0x3c,
};

enum tcrenum3 {
__L4_TCR_PLAT_TLS = 0x30,
x4TCR_PLAT_TLS = 0xc0,
};



// ll.h
struct ll {
    struct ll *next;            /* Head */
    struct ll *prev;            /* Tail */
    void *data;
};

struct double_list {
    struct ll *head;
    struct ll *tail;
};

// binary_tree.h
struct bin_tree_node {
    struct bin_tree_node *left;
    struct bin_tree_node *right;
    char *key;
    void *data;
};

struct bin_tree {
    struct bin_tree_node *root;
};

// syscalls_asm.h
enum syscalls {
SYSCALL_ipc                 =0x0,
SYSCALL_thread_switch       =0x4,
SYSCALL_thread_control      =0x8,
SYSCALL_exchange_registers  =0xc,
SYSCALL_schedule            =0x10,
SYSCALL_map_control         =0x14,
SYSCALL_space_control       =0x18,
SYSCALL_processor_control   =0x1c,
SYSCALL_cache_control       =0x20,
SYSCALL_ipc_control         =0x24,
SYSCALL_lipc                =0x28,

SYSNUM_ipc                 =0xffffff00,
SYSNUM_thread_switch       =0xffffff04,
SYSNUM_thread_control      =0xffffff08,
SYSNUM_exchange_registers  =0xffffff0c,
SYSNUM_schedule            =0xffffff10,
SYSNUM_map_control         =0xffffff14,
SYSNUM_space_control       =0xffffff18,
SYSNUM_processor_control   =0xffffff1c,
SYSNUM_cache_control       =0xffffff20,
SYSNUM_ipc_control         =0xffffff24,
SYSNUM_lipc                =0xffffff28,

SWINUM_ipc                 =0x1400,
SWINUM_thread_switch       =0x1404,
SWINUM_thread_control      =0x1408,
SWINUM_exchange_registers  =0x140c,
SWINUM_schedule            =0x1410,
SWINUM_map_control         =0x1414,
SWINUM_space_control       =0x1418,
SWINUM_processor_control   =0x141c,
SWINUM_cache_control       =0x1420,
SWINUM_ipc_control         =0x1424,
SWINUM_lipc                =0x1428,
};


// kip.h
typedef L4_Word_t L4_KernelId_t;
typedef L4_Word_t L4_ApiVersion_t;
typedef L4_Word_t L4_ApiFlags_t;
typedef L4_Word_t L4_MemoryInfo_t;

struct L4_KernelInterfacePage_struct {
    L4_Word_t magic;
    L4_ApiVersion_t ApiVersion;
    L4_ApiFlags_t ApiFlags;
    L4_Word_t KernelVerPtr;

    /* 0x10 */
    L4_Word_t __padding10[16];
    L4_Word_t MaxMemoryDescs;
    L4_MemoryInfo_t MemoryInfo;
    L4_Word_t __padding58[2];

    /* 0x60 */
    struct {
        L4_Word_t low;
        L4_Word_t high;
    } MainMem;

    /* 0x68 */
    struct {
        L4_Word_t low;
        L4_Word_t high;
    } ReservedMem[2];

    /* 0x78 */
    struct {
        L4_Word_t low;
        L4_Word_t high;
    } DedicatedMem[5];

    /* 0xA0 */
    L4_Word_t SpaceInfo;
    L4_Word_t VirtualRegInfo;
    L4_Word_t UtcbAreaInfo;
    L4_Word_t KipAreaInfo;

    /* 0xB0 */
    L4_Word_t BootInfoVirt;
    L4_Word_t BootInfoEnd;
    L4_Word_t BootInfo;
    L4_Word_t ProcDescPtr;

    L4_Word_t ClockInfo;
    L4_Word_t ThreadInfo;
    L4_Word_t PageInfo;
    L4_Word_t ProcessorInfo;

    /* 0xD0 */
    L4_Word_t MapControl;
    L4_Word_t SpaceControl;
    L4_Word_t ThreadControl;
    L4_Word_t ProcessorControl;
    L4_Word_t CacheControl;

    /* 0xE0 */
    L4_Word_t Ipc;
    L4_Word_t Lipc;
    L4_Word_t ExchangeRegisters;

    /*
     * 0xF0
     */
    L4_Word_t __paddingF0;
    L4_Word_t ThreadSwitch;
    L4_Word_t Schedule;
    L4_Word_t IpcControl;

    /* 0x100 */
    L4_Word_t __padding100[4];

    /* 0x110 */
    L4_Word_t ArchSyscall0;
    L4_Word_t ArchSyscall1;
    L4_Word_t ArchSyscall2;
    L4_Word_t ArchSyscall3;
};




// cb.h
struct cb {
    char *head;
    char *tail;
    char *end;
    char start[1];
};

struct cb_get_handle {
    struct cb *cb;
    char *tail;
};

struct cb_get_handle {
    struct cb *cb;
    char *tail;
};



// session.h
struct session { // XXX where'd I get this one from?
    uintptr_t magic;
    struct pd *owner;
    struct thread *client;
    struct thread *server;
    void *call_buf;
    void *return_buf;
    struct memsection *clist;
    struct session **owner_node;
    struct session **server_node;
    struct session **client_node;
};


struct session2 { // iguana/include/session.h 
    session_ref_t ref;
    cap_t *clist;
    int cap_pos;
    int cap_size;
    int own_clist;
};

// asynch.h
struct asynch {
    uintptr_t asynch_bit;
    uintptr_t object_type;
};



// naming.h
struct naming_session {
    object_t __naming_object;
    uintptr_t naming_sync_mask;
    uintptr_t naming_type;
    struct session __naming_session;
};

struct naming_session {
    object_t __naming_object;
    uintptr_t naming_sync_mask;
    uintptr_t naming_type;
    struct session __naming_session;
};

struct naming_notify_obj {
    struct asynch asynch;
    objref_t obj;
    char name[1];
};

typedef struct naming_notify_obj *naming_notify_t;


// asynch.h

struct tlsplatform { // not really a struct in the code, but implicity L4 TCR TLS stuff */
    int skip0;
    int skip1;
    int skip2;
    uintptr_t __synch_bits;
    uintptr_t asynch_mask;
    struct asynch **asynch_objects;
};

// pd.h
struct clist_list {
    struct clist_node *first;
    struct clist_node *last;
};

struct clist_info {
    cap_t *clist;
    unsigned int type;
    uintptr_t length;
};

struct clist_node {
    struct clist_node *next;
    struct clist_node *prev;
    struct clist_info data;
};

// cap.c
struct clist {
    int slot;
    size_t size;
    size_t cap_free;
    memsection_ref_t clist_memsect;
    cap_t *cap_list;
};

// object.c
typedef struct {
    uintptr_t key;
    objref_t value;
} obj_env_t;
