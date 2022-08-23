bl_info = {
    'name': 'Image Scroller',
    'description': 'Assigns hotkeys for scrolling images in Image Editor',
    'author': 'Pavel_Blend',
    'version': (0, 2, 0),
    'blender': (3, 2, 0),
    'location':
        'Image Editor > Page Up, Page Down, '
        'Shift + Page Up, Shift + Page Down',
    'category': 'UV',
}


import bpy


def set_image_by_index(context, image_index):
    images_count = len(bpy.data.images)
    if not images_count:
        return
    if image_index < images_count:
        bpy_image = bpy.data.images[image_index]
        context.area.spaces[0].image = bpy_image


def get_image_index(context):
    images_count = len(bpy.data.images)
    if not images_count:
        return
    active_image = context.area.spaces[0].image
    if not active_image:
        return
    for image_index, image in enumerate(bpy.data.images):
        if image is active_image:
            return image_index


def get_key_config():
    window_manager = bpy.context.window_manager
    key_config = window_manager.keyconfigs.addon
    return key_config


MODE_NEXT = 'NEXT'
MODE_PREV = 'PREV'
MODE_FIRST = 'FIRST'
MODE_LAST = 'LAST'

keys = ('PAGE_DOWN', 'PAGE_UP', 'PAGE_DOWN', 'PAGE_UP')
shifts = (False, False, True, True)
modes = (MODE_NEXT, MODE_PREV, MODE_LAST, MODE_FIRST)


class IMGSCROLL_OT_scroll_image(bpy.types.Operator):
    bl_idname = 'uv.scroll_image'
    bl_label = 'Scroll Image'

    mode: bpy.props.EnumProperty(
        name='Mode',
        default=MODE_NEXT,
        items=(
            (MODE_NEXT, '', ''),
            (MODE_PREV, '', ''),
            (MODE_FIRST, '', ''),
            (MODE_LAST, '', '')
        )
    )

    @classmethod
    def poll(self, context):
        return context.area.type == 'IMAGE_EDITOR'

    def execute(self, context):
        if self.mode in (MODE_NEXT, MODE_PREV):
            image_index = get_image_index(context)
            if image_index is None:
                image_index = 0
            else:
                if self.mode == MODE_NEXT:
                    image_index += 1
                else:
                    image_index -= 1
        elif self.mode == MODE_FIRST:
            image_index = 0
        elif self.mode == MODE_LAST:
            image_index = -1
        set_image_by_index(context, image_index)
        return {'FINISHED'}


addon_keymaps = []


def add_keymap_item(keymaps, operator, key, mode, shift):
    keymap_item = keymaps.keymap_items.new(
        operator,
        key,
        'PRESS',
        shift=shift,
        repeat=True
    )
    keymap_item.properties.mode = mode
    addon_keymaps.append((keymaps, keymap_item))


def register():
    bpy.utils.register_class(IMGSCROLL_OT_scroll_image)
    key_config = get_key_config()
    if key_config:
        keymaps = key_config.keymaps.new(
            name='Image',
            space_type='IMAGE_EDITOR'
        )
        for key, shift, mode in zip(keys, shifts, modes):
            keymap_item = add_keymap_item(
                keymaps,
                IMGSCROLL_OT_scroll_image.bl_idname,
                key,
                mode,
                shift
            )


def unregister():
    key_config = get_key_config()
    if key_config:
        for keymaps, keymap_item in addon_keymaps:
            keymaps.keymap_items.remove(keymap_item)
    addon_keymaps.clear()
    bpy.utils.unregister_class(IMGSCROLL_OT_scroll_image)
