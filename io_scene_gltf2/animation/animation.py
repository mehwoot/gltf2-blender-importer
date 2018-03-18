"""
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * Contributor(s): Julien Duroure.
 *
 * ***** END GPL LICENSE BLOCK *****
 """

from .animchannel import *

class Animation():
    def __init__(self, index, json, gltf):
        self.index = index
        self.json  = json # Animation json
        self.gltf  = gltf # Reference to global glTF instance
        self.name  = None

        self.channels = []

    def read(self):
        if not 'channels' in self.json.keys():
            return

        channel_idx = 0
        for channel in self.json['channels']:
            chan = AnimChannel(channel_idx, self.json['channels'][channel_idx], self, self.gltf)
            chan.read()
            self.channels.append(chan)
            channel_idx += 1

        self.dispatch_to_nodes()

        if 'name' in self.json.keys():
            self.name = self.json.keys()

    def dispatch_to_nodes(self):
        for channel in self.channels:
            node = self.gltf.get_node(channel.node)
            if node:
                node.set_anim(channel)
            else:
                print("ERROR, node not found")