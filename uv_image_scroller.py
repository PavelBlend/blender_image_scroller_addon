
bl_info = {
    'name': 'Image Scroller',
    'description': 'Assigns hotkeys for scrolling images in UV/Image Editor',
    'author': 'Pavel_Blend',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'UV/Image Editor > Page Up, Page Down, '
                'Shift + Page Up, Shift + Page Down',
    'category': 'UV',
    }


import bpy


def set_last_or_first_image(context, image_index):
    images_count = len(bpy.data.images)
    if images_count > 0:
        active_image = context.area.spaces[0].image
        if active_image:
            image = bpy.data.images[image_index]
            context.area.spaces[0].image = image


class ImageScroller(bpy.types.Operator):
    @classmethod
    def poll(self, context):
        area = context.area.type == 'IMAGE_EDITOR'
        ob = bpy.context.object
        if ob:
            mode = ob.mode == 'OBJECT'
        else:
            mode = True
        return area and mode


class ImageScroller_NextImage(ImageScroller):
    bl_idname = 'uv.next_image'
    bl_label = 'Next Image'

    def execute(self, context):
        images_count = len(bpy.data.images)
        if images_count > 0:
            active_image = context.area.spaces[0].image
            if active_image:
                for image_index, image in enumerate(bpy.data.images):
                    if image.name == active_image.name:
                        break
                image_index += 1
                if image_index < images_count:
                    next_image = bpy.data.images[image_index]
                    context.area.spaces[0].image = next_image
        return {'FINISHED'}


class ImageScroller_PreviousImage(ImageScroller):
    bl_idname = 'uv.previous_image'
    bl_label = 'Previous Image'

    def execute(self, context):
        images_count = len(bpy.data.images)
        if images_count > 0:
            active_image = context.area.spaces[0].image
            if active_image:
                for image_index, image in enumerate(bpy.data.images):
                    if image.name == active_image.name:
                        break
                image_index -= 1
                if image_index >= 0:
                    previous_image = bpy.data.images[image_index]
                    context.area.spaces[0].image = previous_image
        return {'FINISHED'}


class ImageScroller_LastImage(ImageScroller):
    bl_idname = 'uv.last_image'
    bl_label = 'Last Image'

    def execute(self, context):
        set_last_or_first_image(context, -1)
        return {'FINISHED'}


class ImageScroller_FirtsImage(ImageScroller):
    bl_idname = 'uv.first_image'
    bl_label = 'First Image'

    def execute(self, context):
        set_last_or_first_image(context, 0)
        return {'FINISHED'}


addon_keymaps = []


def register():
    bpy.utils.register_class(ImageScroller_NextImage)
    bpy.utils.register_class(ImageScroller_PreviousImage)
    bpy.utils.register_class(ImageScroller_LastImage)
    bpy.utils.register_class(ImageScroller_FirtsImage)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(
            name='Image',
            space_type='IMAGE_EDITOR'
            )
        kmi = km.keymap_items.new('uv.next_image', 'PAGE_DOWN', 'PRESS')
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('uv.previous_image', 'PAGE_UP', 'PRESS')
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(
            'uv.last_image', 'PAGE_DOWN', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(
            'uv.first_image', 'PAGE_UP', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(ImageScroller_NextImage)
    bpy.utils.unregister_class(ImageScroller_PreviousImage)
    bpy.utils.unregister_class(ImageScroller_LastImage)
    bpy.utils.unregister_class(ImageScroller_FirtsImage)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
