#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base widget that shows all available plugins for Artella Launcher
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from Qt.QtCore import *
from Qt.QtWidgets import *

from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts


class PluginButton(base.BaseWidget, object):

    clicked = Signal(object)

    def __init__(self, project, plugin, parent=None):
        self._project = project
        self._plugin = plugin
        super(PluginButton, self).__init__(parent=parent)

    @property
    def name(self):
        """
        Returns the name of the DCC
        :return: str
        """

        return self._name

    def ui(self):
        super(PluginButton, self).ui()

        plugin_name = self._plugin.LABEL
        self._title = QPushButton(plugin_name)
        self._title.setStyleSheet(
            """
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            """
        )
        self._title.setFixedHeight(20)

        self.main_layout.addWidget(self._title)
        self._plugin_btn = QPushButton()
        self._plugin_btn.setFixedSize(QSize(100, 100))
        self._plugin_btn.setIconSize(QSize(110, 110))
        self._plugin_btn.setIcon(self._plugin.get_icon())
        self._plugin_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.main_layout.addWidget(self._plugin_btn)

    def setup_signals(self):
        self._title.clicked.connect(self._on_button_clicked)
        self._plugin_btn.clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self):
        self.clicked.emit(self._plugin)


class PluginsPanel(base.BaseWidget, object):

    openPlugin = Signal(object)
    closeLauncher = Signal()

    def __init__(self, project, parent=None):

        self._project = project

        super(PluginsPanel, self).__init__(parent=parent)

    def ui(self):
        super(PluginsPanel, self).ui()

        self._flow_layout = layouts.FlowLayout()
        self.main_layout.addLayout(self._flow_layout)

    def add_plugin(self, plugin):
        """
        Adds a new plugin to the panel
        :param plugin: ArtellaLauncherPlugin
        """

        if not plugin:
            return

        plugin_btn = PluginButton(project=self._project, plugin=plugin)
        plugin_btn.clicked.connect(self.openPlugin.emit)
        self._flow_layout.addWidget(plugin_btn)
