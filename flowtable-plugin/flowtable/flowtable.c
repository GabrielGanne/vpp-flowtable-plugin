/*
 * Copyright (c) 2016 Qosmos and/or its affiliates.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "flowtable.h"
#include <vnet/plugin/plugin.h>

flowtable_main_t flowtable_main;

int
flowtable_enable_disable(flowtable_main_t * fm,
    u32 sw_if_index, int enable_disable)
{
    u32 node_index = enable_disable ? flowtable_node.index : ~0;

    return vnet_hw_interface_rx_redirect_to_node(fm->vnet_main,
            sw_if_index, node_index);
}

static clib_error_t *
flowtable_enable_disable_command_fn(vlib_main_t * vm,
    unformat_input_t * input, vlib_cli_command_t * cmd)
{
    flowtable_main_t * fm = &flowtable_main;
    u32 sw_if_index = ~0;
    int enable_disable = 1;
    u32 next_node_index = ~0;
    u32 flows_max = ~0;
    int rv = 0;

    while (unformat_check_input(input) != UNFORMAT_END_OF_INPUT)
    {
        if (unformat(input, "disable"))
            enable_disable = 0;
        else if (unformat(input, "next-node %U", unformat_vlib_node,
            fm->vnet_main, &next_node_index))
            ;
        else if (unformat(input, "max-flows %u", &next_node_index))
            ;
        else if (unformat(input, "intf %U", unformat_vnet_sw_interface,
            fm->vnet_main, &sw_if_index))
            ;
        else
            break;
    }

    /* by default, leave the packet follow its course */
    if (next_node_index != ~0)
        fm->next_node_index = next_node_index;
    else
        fm->next_node_index = FT_NEXT_ETHERNET_INPUT;

    if (sw_if_index != ~0)
        rv = flowtable_enable_disable(fm, sw_if_index, enable_disable);

    if (flows_max != ~0) {
        if (fm->flows_max < flows_max) {
            pool_alloc_aligned(fm->flows, flows_max - fm->flows_max, CLIB_CACHE_LINE_BYTES);
        }
        fm->flows_max = flows_max;
    }

    switch (rv) {
      case 0:
          break;
      case VNET_API_ERROR_INVALID_SW_IF_INDEX:
          return clib_error_return(0, "Invalid interface");
      case VNET_API_ERROR_UNIMPLEMENTED:
          return clib_error_return(0,
                "Device driver doesn't support redirection");
      default:
          return clib_error_return(0, "flowtable_enable_disable returned %d",
                rv);
    }

    return 0;
}

VLIB_CLI_COMMAND(flowtable_interface_enable_disable_command) = {
    .path = "flowtable",
    .short_help = "flowtable [max-flows <n>] [intf <name>] [next-node <name>] [disable]",
    .function = flowtable_enable_disable_command_fn,
};
