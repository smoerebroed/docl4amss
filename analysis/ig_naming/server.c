


/* only slightly different than okl4 1.4.1.1 */
void
server_loop()
    /*
     * l4tag bit layout: llll llll, llll llll, ffff rrrr, rruu uuuu
     * l:label, f:flags, r:res, u:u
    */
    int *mr;            // r4 reg
    l4tag tag;          // sp+0
    l4thread partner;   // sp+4

    partner = 0;
    mr = L4_MRStart(); // utcb + 0x40

    while(1) {
        check_async()
        tag = mr[0]; // L4_MRStart() inlined here again for some reason
        tag.flags &= 0x7;

        l4tag tagw = tag;   // r12 reg
        tagw.flags |= L4_Waittag; // 0x4
        L4_Ipc(peer, L4_anythread, tagw, &peer); // anythread = -1

        if(msg_is_error(mr[0])) {
            puts("server: error sending IPC reply");
            partner = 0;
            continue;
        }
        if(mr[1] == 43) {
            dispatch_naming_read(&partner, mr);
        } else if(mr[1] == 42) {
           dispatch_naming_write(&partner, mr);
        } else if(mr[1] == 44) {
            dispatch_naming_notify(&partner, mr);
        }
    }
}


int
dispatch_naming_read(l4thread *partner, int *mr)
{
    tag = mr[0]
    int func = tag.label & 0x3f; // r1 reg, sp+0x20

    if(func == 0) { // handle_naming_read_lookup inlined here
        char *p = &mr[3];
        while(*p) p++; // results not used

        var20 = 0;
        ret = naming_read_lookup_impl(*partner, mr[2], &mr[3], &var20);
        if(var20 == 0) {
            mr[0] = 2;
            mr[1] = ret
        } else {
            *partner = 0;
            mr[0] &= 0xffffff00; // store first byte zero
        }
    } else if(func == 1) { // handle_naming_read_notify inlined here
        var1c = mr[4]; // part of var18 structure?
        var10 = 0

        char *p = &mr[6];
        while(*p) p++; // result not used

        // XXX why is this so odd?
        // is this due to some object references being passed?
        // this differs considerably from the 1.4.1.1 version...
        ret = naming_read_notify_impl(*partner, mr[2], &mr[6], mr[3], &var1c,  mr[6], &var18, &var10);
        if(var10 == 0) {
            mr[0] = 3;
            mr[1] = var18
            mr[2] = ret
        } else {
            *partner = 0;
            mr[0] &= 0xffffff00; // store first byte zero
        }
    }
    return 0;
}

