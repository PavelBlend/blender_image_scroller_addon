bl_info = {
    'name': 'Image Scroller',
    'description': 'Assigns hotkeys for scrolling images in Image Editor',
    'author': 'Pavel_Blend',
    'version': (0, 1, 0),
    'blender': (2, 80, 0),
    'location':
        'Image Editor > Page Up, Page Down, '
        'Shift + Page Up, Shift + Page Down',
    'category': 'UV',
}


import bpy


def set_image_by_index(context, image_index):
    images_count = len(bpy.data.images)
    if images_count > 0:
        bpy_image = bpy.data.images[image_index]
        context.area.spaces[0].image = bpy_image


def get_image_index(context):
    images_count = len(bpy.data.images)
    if images_count > 0:
        active_image = context.area.spaces[0].image
        if active_image:
            for image_index, image in enumerate(bpy.data.images):
                if image.name == active_image.name:
                    return image_index, images_count
    return None, None


class BaseOperator(bpy.types.Operator):
    @classmethod
    def poll(self, context):
        is_image_editor = context.area.type == 'IMAGE_EDITOR'
        return is_image_editor


class IMGSCROLL_OT_next_image(BaseOperator):
    bl_idname = 'uv.next_image'
    bl_label = 'Image Scroller: Next Image'

    def execute(self, context):
        image_index, images_count = get_image_index(context)
        if not (image_index is None):
            image_index += 1
            if image_index < images_count:
                next_image = bpy.data.images[image_index]
                context.area.spaces[0].image = next_image
        else:
            bpy.ops.uv.first_image()
        return {'FINISHED'}


class IMGSCROLL_OT_prev_image(BaseOperator):
    bl_idname = 'uv.prev_image'
    bl_label = 'Image Scroller: Previous Image'

    def execute(self, context):
        image_index, images_count = get_image_index(context)
        if not (image_index is None):
            image_index -= 1
            if image_index >= 0:
                prev_image = bpy.data.images[image_index]
                context.area.spaces[0].image = prev_image
        else:
            bpy.ops.uv.first_image()
        return {'FINISHED'}


class IMGSCROLL_OT_last_image(BaseOperator):
    bl_idname = 'uv.last_image'
    bl_label = 'Image Scroller: Last Image'

    def execute(self, context):
        set_image_by_index(context, -1)
        return {'FINISHED'}


class IMGSCROLL_OT_first_image(BaseOperator):
    bl_idname = 'uv.first_image'
    bl_label = 'Image Scroller: First Image'

    def execute(self, context):
        set_image_by_index(context, 0)
        return {'FINISHED'}


addon_keymaps = []
operators = (
    IMGSCROLL_OT_next_image,
    IMGSCROLL_OT_prev_image,
    IMGSCROLL_OT_last_image,
    IMGSCROLL_OT_first_image
)


def add_keymap_item(keymaps, operator, key, shift=False):
    keymap_item = keymaps.keymap_items.new(
        operator,
        key,
        'PRESS',
        shift=shift,
        repeat=True
    )
    addon_keymaps.append((keymaps, keymap_item))


def register():
    for operator in operators:
        bpy.utils.register_class(operator)
    window_manager = bpy.context.window_manager
    key_config = window_manager.keyconfigs.addon
    if key_config:
        keymaps = key_config.keymaps.new(
            name='Image',
            space_type='IMAGE_EDITOR'
        )
        # next
        keymap_item = add_keymap_item(
            keymaps,
            IMGSCROLL_OT_next_image.bl_idname,
            'PAGE_DOWN'
        )
        # prev
        keymap_item = add_keymap_item(
            keymaps,
            IMGSCROLL_OT_prev_image.bl_idname,
            'PAGE_UP'
        )
        # last
        keymap_item = add_keymap_item(
            keymaps,
            IMGSCROLL_OT_last_image.bl_idname,
            'PAGE_DOWN',
            shift=True
        )
        # first
        keymap_item = add_keymap_item(
            keymaps,
            IMGSCROLL_OT_first_image.bl_idname,
            'PAGE_UP',
            shift=True
        )


def unregister():
    window_manager = bpy.context.window_manager
    key_config = window_manager.keyconfigs.addon
    if key_config:
        for keymaps, keymap_item in addon_keymaps:
            keymaps.keymap_items.remove(keymap_item)
    addon_keymaps.clear()
    for operator in reversed(operators):
        bpy.utils.unregister_class(operator)
