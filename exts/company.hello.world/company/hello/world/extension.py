from ctypes import alignment
import omni.ext
import omni.ui as ui
import omni.kit.asset_converter as converter
from pxr import UsdUtils
from omni import usd
import asyncio


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[company.hello.world] MyExtension startup")

        def progress_callback(current, total):
            print("progress " + current + ", " + total)

        async def convert(stage_id):
            task_manger = converter.get_instance()
            task = task_manger.create_converter_task(
                import_path=stage_id, output_path="e:\\test.glb", progress_callback=lambda: progress_callback()
            )

            success = await task.wait_until_finished()
            if not success:
                detailed_status_code = task.get_status()
                detailed_status_error_string = task.get_error_message()
                print("error " + detailed_status_code + " " + detailed_status_error_string)

        def on_click():
            print("[company.hello.world] clicking")

            main_stage = usd.get_context().get_stage()
            stage_id = UsdUtils.StageCache.Get().GetId(main_stage).ToString()

            print("converting " + stage_id)

            asyncio.ensure_future(convert(stage_id))

            print("[company.hello.world] clicked!")

        self._window = ui.Window("AWS IoT TwinMaker Plugin", width=300, height=300)
        with self._window.frame:
            with ui.VStack(spacing=10):
                with ui.HStack(height=0):
                    ui.Spacer(width=10)
                    ui.Label("Workspace", width=0)
                    ui.Spacer(width=10)
                    ui.ComboBox(0, "Workspace1", "Workspace2")

                ui.Button("Convert to GLTF", height=0, clicked_fn=lambda: on_click())

                ui.IntField(height=0)

    def on_shutdown(self):
        print("[company.hello.world] MyExtension shutdown")
