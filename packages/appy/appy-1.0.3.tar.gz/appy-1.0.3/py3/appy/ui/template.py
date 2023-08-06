'''Base template for any UI page'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2020 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from appy.px import Px

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Template:
    # The template of all base PXs
    px = Px('''
     <html var="x=handler.customInit(); cfg=config.ui" dir=":dir">

      <head>
       <title>:tool.getPageTitle(home)</title>
       <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
       <link rel="icon" type="image/x-icon"
             href=":url('favicon.ico', base=appName)"/>
       <link rel="apple-touch-icon" href=":url('appleicon', base=appName)"/>
       <x>::ui.Includer.getGlobal(handler, config, dir)</x>
      </head>

      <body class=":cfg.getClass('body', _px_, _ctx_)"
            var="showPortlet=ui.Portlet.show(tool, _px_, _ctx_);
                 showSidebar=ui.Sidebar.show(tool, o, layout, popup);
                 bi=ui.Browser.getIncompatibilityMessage(tool, handler)">

       <!-- The browser incompatibility message -->
       <div if="bi" class="wrongBrowser">::bi</div>

       <!-- Google Analytics stuff, if enabled -->
       <script var="gaCode=tool.getGoogleAnalyticsCode(handler, config)"
               if="gaCode">:gaCode</script>

       <!-- Popups -->
       <x>::ui.Globals.getPopups(tool, url, _, dleft, dright, popup)</x>

       <div class=":cfg.getClass('main', _px_, _ctx_)"
            style=":cfg.getBackground(_px_, siteUrl, type='home')">

        <!-- Header -->
        <div class="top" if="cfg.showHeader(_px_, _ctx_, popup)"
             style=":cfg.getBackground(_px_, siteUrl, type='header')">

         <!-- Icons and messages @left -->
         <div class="headerMessages">

          <!-- The burger button for collapsing the portlet -->
          <a if="showPortlet" class="clickable"
             onclick="toggleCookie('appyPortlet','block','expanded',\
                'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>

          <!-- The home icon -->
          <a if="not isAnon" href=":tool.computeHomePage()">
            <img src=":url('home.svg')" class="icon"/></a>

          <!-- Header messages -->
          <span class="headerText" var="text=cfg.getHeaderText(tool)"
                if="not popup and text">::text</span>
         </div>

         <!-- Links and icons @right -->
         <div class="headerLinks" align=":dright">

          <!-- Custom links -->
          <x>:tool.pxLinks</x>

          <!-- Connect link if discreet login -->
          <a if="isAnon and cfg.discreetLogin" id="loginIcon"
             name="loginIcon" onclick="toggleLoginBox(true)" class="clickable">
           <img src=":url('login.svg')" class="icon"
                title=":_('app_connect')"/></a>

          <!-- Root pages -->
          <x var="pages=tool.getRootPages()"
             if="pages">:tool.OPage.pxSelector</x>

          <!-- Language selector -->
          <x if="ui.Language.showSelector(cfg, \
                                          layout)">:ui.Language.pxSelector</x>

          <!-- User info and controls for authenticated users -->
          <x if="not isAnon">
           <!-- Config -->
           <a if="cfg.showTool(tool)" href=":'%s/view' % tool.url"
                  title=":_('Tool')">
            <img src=":url('config.svg')" class="icon"/></a>
           <x>:user.pxUserLink</x>
           <!-- Log out -->
           <a href=":guard.getLogoutUrl(tool, user)" title=":_('app_logout')">
            <img src=":url('logout.svg')" class="icon"/></a>
          </x>
          <!-- Custom links at the end of the list -->
          <x>:tool.pxLinksAfter</x>

          <!-- The burger button for collapsing the sidebar -->
          <a if="showSidebar" class="clickable"
             onclick="toggleCookie('appySidebar','block','expanded',\
                'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>
         </div>

        </div>
        <div height="0">:ui.Message.px</div> <!-- The message zone -->

        <!-- The login zone -->
        <x if="isAnon and not o.isTemp() and not bi">:guard.pxLogin</x>

        <!-- The main zone: portlet, content and sidebar -->
        <div class=":'payload payloadP' if popup else 'payload'">

         <!-- The portlet -->
         <x if="showPortlet">:ui.Portlet.px</x>

         <!-- Page content -->
         <div class=":'contentP' if popup else 'content'">:content</div>

         <!-- The sidebar -->
         <x if="showSidebar">:ui.Sidebar.px</x>
        </div>

        <!-- Footer -->
        <x if="cfg.showFooter(_px_, _ctx_, popup)">::ui.Footer.px</x>
       </div>
      </body>
     </html>''', prologue=Px.xhtmlPrologue)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
