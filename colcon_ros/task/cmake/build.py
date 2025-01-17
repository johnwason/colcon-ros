# Copyright 2016-2018 Dirk Thomas
# Licensed under the Apache License, Version 2.0


from colcon_cmake.task.cmake.build import CmakeBuildTask as CmakeBuildTask_
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.task import TaskExtensionPoint
from colcon_ros.task import add_app_to_cpp
from colcon_core import __version__ as colcon_core_version
from os import environ

logger = colcon_logger.getChild(__name__)


class CmakeBuildTask(TaskExtensionPoint):
    """Build ROS packages with the build type 'cmake'."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    async def build(self):  # noqa: D102
        args = self.context.args
        logger.info(
            "Building ROS package in '{args.path}' with build type 'cmake'"
            .format_map(locals()))

        # reuse CMake build task with additional logic
        extension = CmakeBuildTask_()
        extension.set_context(context=self.context)

        # Add extra CMake variables to help packages detect ROS
        if self.context.args.cmake_args is None:
            self.context.args.cmake_args = []
        self.context.args.cmake_args += ['-D' + 'COLCON_VERSION:STRING='
                                         + str(colcon_core_version)]
        if 'ROS_VERSION' in environ:
            self.context.args.cmake_args += ['-D'
                                             + 'COLCON_ROS_VERSION:STRING='
                                             + environ['ROS_VERSION']]
        if 'ROS_DISTRO' in environ:
            self.context.args.cmake_args += ['-D'
                                             + 'COLCON_ROS_DISTRO:STRING='
                                             + environ['ROS_DISTRO']]

        return await extension.build(environment_callback=add_app_to_cpp)
