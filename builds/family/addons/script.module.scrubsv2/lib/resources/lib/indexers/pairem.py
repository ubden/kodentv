# -*- coding: UTF-8 -*-

import os,time,xbmc,xbmcgui,urllib2,webbrowser


def pairmenuoptions():
    dialog = xbmcgui.Dialog()
    funcs = (
        pairfunction1,
        pairfunction2,
        pairfunction3,
		pairfunction4,
		pairfunction5,
		pairfunction6,
		pairfunction7,
		pairfunction8,
		pairfunction9,
		pairfunction10,
		pairfunction11,
		pairfunction12,
		pairfunction13,
		pairfunction14,
		)


    call = dialog.select('[B][COLOR=grey]Pair Em[/COLOR][/B]', [
        '[B][COLOR=purple]            OpenLoad[/COLOR][/B]',
        '[B][COLOR=purple]            Streamango[/COLOR][/B]',
        '[B][COLOR=purple]            TheVideo[/COLOR][/B]',
        '[B][COLOR=purple]            StreamCherry[/COLOR][/B]',
        '[B][COLOR=purple]            VidUpMe[/COLOR][/B]',
        '[B][COLOR=purple]            Vevio[/COLOR][/B]',
        '[B][COLOR=purple]            vShare[/COLOR][/B]',
        '[B][COLOR=purple]            FlashX[/COLOR][/B]',
        '[B][COLOR=grey]            Trakt SignUp[/COLOR][/B]',
        '[B][COLOR=grey]            TMDB SignUp[/COLOR][/B]',
        '[B][COLOR=grey]            IMDB SignUp[/COLOR][/B]',
        '[B][COLOR=grey]            RealDebrid SignUp[/COLOR][/B]',
        '[B][COLOR=grey]            Authorize RealDebrid[/COLOR][/B]',
        '[B][COLOR=purple]            Cancel & Close[/COLOR][/B]',])


    # dialog.selectreturns
    #   0 -> escape pressed
    #   1 -> first item
    #   2 -> second item
    if call:
        # esc is not pressed
        if call < 0:
            return
        func = funcs[call-14] # Number of functions (function15)
        return func()
    else:
        func = funcs[call]
        return func()
    return


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
myplatform = platform()


def pairfunction1():
    if myplatform == 'android': # OpenLoad
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://olpair.com/pair' ) )
    else:
        opensite = webbrowser . open('https://olpair.com/pair')


def pairfunction2():
    if myplatform == 'android': # StreaMango
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://streamango.com/pair' ) )
    else:
        opensite = webbrowser . open('https://streamango.com/pair')


def pairfunction3():
    if myplatform == 'android': # TheVideo
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://thevideo.me/pair' ) )
    else:
        opensite = webbrowser . open('https://thevideo.me/pair')


def pairfunction4():
    if myplatform == 'android': # StreamCherry
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://streamcherry.com/pair' ) )
    else:
        opensite = webbrowser . open('https://streamcherry.com/pair')


def pairfunction5():
    if myplatform == 'android': # VidUp
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://vidup.me/pair' ) )
    else:
        opensite = webbrowser . open('https://vidup.me/pair')


def pairfunction6():
    if myplatform == 'android': # Vevio
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://vev.io/pair' ) )
    else:
        opensite = webbrowser . open('https://vev.io/pair')


def pairfunction7():
    if myplatform == 'android': # vShare
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://vshare.eu/pair' ) )
    else:
        opensite = webbrowser . open('https://vshare.eu/pair')


def pairfunction8():
    if myplatform == 'android': # FlashX
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php' ) )
    else:
        opensite = webbrowser . open('https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php')


def pairfunction9():
    if myplatform == 'android': # Trakt SignUp
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://trakt.tv/join' ) )
    else:
        opensite = webbrowser . open('https://trakt.tv/join')


def pairfunction10():
    if myplatform == 'android': # TMDB SignUp
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.themoviedb.org/account/signup' ) )
    else:
        opensite = webbrowser . open('https://www.themoviedb.org/account/signup')


def pairfunction11():
    if myplatform == 'android': # IMDB SignUp
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://m.imdb.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_mobile_web_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl9tb2JpbGVfd2ViX3VzIiwicmVkaXJlY3RUbyI6Imh0dHA6Ly9tLmltZGIuY29tLz9yZWZfPW1fbG9naW4ifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&&tag=imdbtag_reg-20' ) )
    else:
        opensite = webbrowser . open('https://m.imdb.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_mobile_web_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl9tb2JpbGVfd2ViX3VzIiwicmVkaXJlY3RUbyI6Imh0dHA6Ly9tLmltZGIuY29tLz9yZWZfPW1fbG9naW4ifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&&tag=imdbtag_reg-20')


def pairfunction12():
    if myplatform == 'android': # RealDebrid SignUp
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://real-debrid.com' ) )
    else:
        opensite = webbrowser . open('https://real-debrid.com/')


def pairfunction13():
    if myplatform == 'android': # RealDebrid Authorize
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://real-debrid.com/device' ) )
    else:
        opensite = webbrowser . open('https://real-debrid.com/device')


def pairfunction14(): 0 #Cancel & Close

