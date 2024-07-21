"""
Contains definitions for the Pygame Zero related APIs so they can be
used in the editor for autocomplete and call tips.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


PYGAMEZERO_APIS = {
    'en_US': [
        _('actor.transform_anchor(ax, ay, w, h, angle) \n\nTransform anchor based upon a rotation of a surface of size w x h.'),
        _('animation.animate(object, tween=\'linear\', duration=1, on_finished=None, **targets) \n\nAn animation manager for object attribute animations.\n\nEach keyword argument given to the Animation on creation (except\n"type" and "duration") will be *tweened* from their current value\non the object to the target value specified.\n\nIf the value is a list or tuple, then each value inside that will\nbe tweened.\n\nThe update() method is automatically scheduled with the clock for\nthe duration of the animation.'),
        _('clock.Clock() \n\nA clock used for event scheduling.\n\nWhen tick() is called, all events scheduled for before now will be called\nin order.\n\ntick() would typically be called from the game loop for the default clock.\n\nAdditional clocks could be created - for example, a game clock that could\nbe suspended in pause screens. Your code must take care of calling tick()\nor not. You could also run the clock at a different rate if desired, by\nscaling dt before passing it to tick().'),
        _('clock.Event(time, cb, repeat=None) \n\nAn event scheduled for a future time.\n\nEvents are ordered by their scheduled execution time.'),
        _('clock.each_tick(callback) \n\nSchedule a callback to be called every tick.\n\nUnlike the standard scheduler functions, the callable is passed the\nelapsed clock time since the last call (the same value passed to tick).'),
        _('clock.schedule(callback, delay) \n\nSchedule callback to be called once, at `delay` seconds from now.\n\n:param callback: A parameterless callable to be called.\n:param delay: The delay before the call (in clock time / seconds).'),
        _('clock.schedule_interval(callback, delay) \n\nSchedule callback to be called every `delay` seconds.\n\nThe first occurrence will be after `delay` seconds.\n\n:param callback: A parameterless callable to be called.\n:param delay: The interval in seconds.'),
        _('clock.schedule_unique(callback, delay) \n\nSchedule callback to be called once, at `delay` seconds from now.\n\nIf it was already scheduled, postpone its firing.\n\n:param callback: A parameterless callable to be called.\n:param delay: The delay before the call (in clock time / seconds).'),
        _('clock.tick(dt) \n\nUpdate the clock time and fire all scheduled events.\n\n:param dt: The elapsed time in seconds.'),
        _('clock.unschedule(callback) \n\nUnschedule the given callback.\n\nIf scheduled multiple times all instances will be unscheduled.'),
        _("clock.weak_method(method) \n\nQuick weak method ref in case users aren't using Python 3.4"),
        _("keyboard.Keyboard() \n\nThe current state of the keyboard.\n\nEach attribute represents a key. For example, ::\n\n    keyboard.a\n\nis True if the 'A' key is depressed, and False otherwise."),
        _('music.fadeout(seconds) \n\nFade out and eventually stop the music playback.\n\n:param seconds: The duration in seconds over which the sound will be faded\n                out. For example, to fade out over half a second, call\n                ``music.fadeout(0.5)``.'),
        _('music.get_pos() \n\nget_pos() -> time\nget the music play time'),
        _('music.get_volume() \n\nget_volume() -> value\nget the music volume'),
        _('music.is_playing(name) \n\nReturn True if the music is playing and not paused.'),
        _('music.pause() \n\nTemporarily stop playback of the music stream.\n\nCall `unpause()` to resume.'),
        _('music.play(name) \n\nPlay a music file from the music/ directory.\n\nThe music will loop when it finishes playing.'),
        _('music.play_once(name) \n\nPlay a music file from the music/ directory.'),
        _('music.queue(name) \n\nQueue a music file to follow the current track.\n\nThis will load a music file and queue it. A queued music file will begin as\nsoon as the current music naturally ends. If the current music is ever\nstopped or changed, the queued song will be lost.'),
        _('music.rewind() \n\nrewind() -> None\nrestart music'),
        _('music.set_pos() \n\nset_pos(pos) -> None\nset position to play from'),
        _('music.set_volume() \n\nset_volume(volume) -> None\nset the music volume'),
        _('music.stop() \n\nstop() -> None\nstop the music playback'),
        _('music.unpause() \n\nResume playback of the music stream after it has been paused.'),
        _('screen.Screen(surface) \n\nInterface to the screen.'),
        _('screen.SurfacePainter(screen) \n\nInterface to pygame.draw that is bound to a surface.'),
        _('screen.round_pos(pos) \n\nRound a tuple position so it can be used for drawing.'),
    ],
    'ko': [
        _('animation.animate(Actor객체, [pos=필수아님], [tween=필수아님], [duration=필수아님], [on_finished=필수아님], [기타 설정값]) \n\nActor객체를 애니메이션 합니다.\npos=이동할 위치\ntween=애니메이션 방법, 예를들어, \'linear\', \'accelerate\' 등\nduration=시간(초)\non_finished=애니메이션 종료시 호출 함수명'),
        _("draw.filled_rect(rect, (R, G, B 색상값)) \n\n채워진 직사각형을 그립니다. 위치로 Rect 객체를 취합니다.\n예를 들어 Rect((x좌표, y좌표), (가로길이, 세로길이))"),
        _("draw.text(텍스트, 위치, [기타 설정값들]) \n\n텍스트를 지정된 위치에 나타냅니다. 텍스트 위치 지정 및 서식 지정을 위한 매우 풍부한 API가 있습니다.\n자세한 내용은 Pygame Zero 라이브러리 메뉴얼을 참조하세요."),
        _("draw.textbox(텍스트, rect, [기타 설정값들]) \n\n주어진 Rect를 채울 크기의 텍스트를 출력합니다. 텍스트 위치 지정 및 서식 지정을 위한 매우 풍부한 API가 있습니다.\n자세한 내용은 Pygame Zero 라이브러리 메뉴얼을 참조하세요."),
        _("screen.blit(이미지, (화면좌측 좌표, 화면상단 좌표)) \n\n주어진 위치에 이미지를 화면에 그립니다. 이미지 매개변수로 Surface 또는 문자열을 허용합니다.\n이미지가 문자열이면 지정된 이미지가 images/ 폴더에서 로드됩니다."),
        _("screen.fill((R, G, B 색상값)| 16진수 색상값 | 색상 키워드)) \n\n게임화면을 주어진 색상으로 채웁니다."),
        _("actor.Actor(이미지 파일명, [pos(화면표시 좌표값)=None], [anchor(객체의 중심값)=None], [기타 설정값들]) \n\nActor 객체를 생성합니다. 생성시 객체의 이미지 파일은 필수이나, 나머지 값들은 객체생성 추후에 개별적으로 설정할 수 있습니다."),
        _("actor.scale : Actor 이미지의 크기 스케일을 설정합니다."),
        _("actor.draw() : Actor를 화면에 출력합니다."),
        _("actor.say_for_sec(텍스트, 시간(초), [전경색=필수아님], [배경색=필수아님], [기타 설정값들]) \n\nActor 이미지 위에 텍스트를 정해진 시간(초) 동안 보여줍니다."),
        _("actor.pos : Actor의 anchor(중심) 좌표값"),
        _("actor.anchor : Actor 중심의 좌표값"),
        _("actor.flip_x : Actor 이미지를 x 방향으로 뒤집기"),
        _("actor.flip_y : Actor 이미지를 y 방향으로 뒤집기"),
        _("actor.angle : Actor 이미지를 특정 각도로 회전시키기"),
        _("actor.images : Actor 객체의 애니메이션을 위한 이미지 그룹 설정"),
        _("actor.next_image() \n\nActor 객체에 할당된 여러 이미지 중 다음 이미지로 이동시킵니다."),
        _("actor.move_forward(이동값) \n\nActor 객체의 angle값을 전방 기준점으로 삼아 할당된 값만큼 전방으로 이동시킵니다."),
        _("actor.move_back(이동값) \n\nActor 객체의 angle값을 전방 기준점으로 삼아 할당된 값만큼 후방으로 이동시킵니다."),
        _("actor.move_left(이동값) \n\nActor 객체의 angle값을 전방 기준점으로 삼아 할당된 값만큼 좌측으로 이동시킵니다."),
        _("actor.move_right(이동값) \n\nActor 객체의 angle값을 전방 기준점으로 삼아 할당된 값만큼 우측으로 이동시킵니다."),
        _("actor.brush_init(스케치 영역, 두께, [색깔=필수아님]) \n\n스케치할 영역, 브러시의 두께와 색상 등을 설정합니다."),
        _("actor.brush_draw() \n\n그리기를 시작합니다."),
        _("actor.brush_stop() \n\n그리기를 멈춥니다."),
        _("actor.brush_clear() \n\n스케치영역을 모두 지웁니다."),
        _("actor.colliderect(오브젝트) -> bool \n\nRect에 기반해 두 오브젝트의 충돌을 검사합니다."),
        _("actor.collide_pixel(오브젝트) -> (Tuple[int, int] | None) \n\n픽셀에 기반해 두 오브젝트의 충돌을 검사합니다."),
        _("actor.collidepoint_pixel(좌표값) -> int \n\n픽셀에 기반에 입력된 좌표와 오브젝트와의 충돌을 검사합니다."),
        _("game.exit() \n\n프로그램을 종료한다."),
        _("sounds.play([재생횟수=필수아님]) \n\n소리를 설정한 횟수만큼 재생합니다. 횟수 미설정시 단회 재생합니다."),
        _("pygame.display.update([Rect=필수아님]) \n\n설정한 Rect의 영역의 화면을 갱신합니다.영역 미설정시 전체화면을 갱신합니다."),
    ],
    'uz_UZ': [
        _("animation.animate(Actor obyekti, [pos=Shart emas], [duration=Shart emas], [tween=Shart emas], [on_finished=Shart emas], [boshqa sozlamalar])\n\nActorni animatsiya qiladi.\npos=Sozilangan joylashuvigacha ko'chirish animatsiyasi qiladi.\ntween=Animatsiya usuli, masalan \'linear\', \'accelerate\' va boshqalar.\nduration=Vaqt (sekund)\non_finished=Animatsiya tugashi bilan chaqirilaydigan funksiya nomi"),
        _("draw.filled_rect(rect, (R, G, B qiymati)) \n\nToʻldirilgan toʻrtburchak chizadi. Rect obyekti orqali jolashuvni oladi.\nMasalan, Rect((x-koordinata, y-koordinata), (kenglik, balandlik ))"),
        _("draw.text(text, joy, [boshqa sozlamalar])\n\nTextni belgilangan joyda chiqaradi. Textni joylashtirish va formatlash uchun juda boy API mavjud.\nBatafsil maʼlumot uchun Pygame Zero kutubxonasining qo'llanmasini qarang."),
        _("draw.textbox(text, rect, [boshqa sozlamalar]) \n\nBerilgan Rectni to'ldiradigan o'lchamdagi textni chiqaradi. Textni joylashtirish va formatlash uchun juda boy API mavjud.\nBatafsil maʼlumot uchun Pygame Zero kutubxonasining qo'llanmasini qarang."),
        _("screen.blit(rasm, (ekran chap koordinatasi, ekranning yuqori koordinatasi)) \n\nEkranda rasmni berilgan joyda chizadi. Surface yoki matnli qiymatini rasm parametri sifatida qabul qiladi.\nAgar rasm matnli qiymati boʻlsa, u images/papkadan yuklab oladi."),
        _("screen.fill((R, G, B qiymati) | rang texti)) \n\nEkranni sozlangan rang bilan to'ldiring." ),
        _("actor.Actor(rasm fayli, [pos(joylashuv)=Shart emas], [anchor(markaz)=Shart emas)], [boshqa sozlamalar]) \n\nActor obyektni yaratadi. Obyektni yaratishda rasm fayli talab qilinadi,\nammo qolgan qiymatlar obyekt yaratilgandan keyin alohida sozlash mumkin."),
        _("actor.scale : Actor rasmining masshtabini sozlash."),
        _("actor.say_for_sec(gap, soniya, [old rangi=Shart emas], [orqa rangi=Shart emas], [boshqa sozlamalar]) \n\nActor rasmining ustida sozlangan soniya davomida gapni ko'rsatadi."),
        _("actor.pos : Actor joylashuvini sozlash. Lekin anchor qiymatiga asoslanadi."),
        _("actor.anchor : Actor markazini sozlash."),
        _("actor.draw() : Actorni ekranga chiqaradi."),
        _("actor.flip_x : True bo'la Actor rasmini x yo'nalishida chappa qiladi."),
        _("actor.flip_y : True bo'lsa Actor rasmini y yo'nalishida chappa qiladi."),
        _("actor.angle : Actor rasmini sozlagan burchakga aylantiradi."),
        _("actor.images : Actor ni animatsiya qilish uchun rasmining guruhini sozlash."),
        _("actor.next_image() \n\nActor rasmlarning guruhidagi keyingi tartibli rasmga o'tadi."),
        _("actor.move_forward(masofa) \n\nActor sozlangan masofa soniga qarab to'g'ri tomoniga yuradi."),
        _("actor.move_back(masofa) \n\nActor sozlangan masofa soniga qarab orqa tomoniga yuradi."),
        _("actor.move_left(masofa) \n\nActor sozlangan masofa soniga qarab chap tomoniga yuradi."),
        _("actor.move_right(masofa) \n\nActor sozlangan masofa soniga qarab o'ng tomoniga yuradi."),
        _("actor.brush_init(maydon, qalinlik, [rang=Shart emas]) \n\nCho'tka qancha maydon ichida qancha qalinlik bilan chizish kerakligini  sozlaydi."),
        _("actor.brush_draw() \n\nCho'tka chizishni boshlaydi."),
        _("actor.brush_stop() \n\nCho'tka chizishni tuxtaydi."),
        _("actor.brush_clear() \n\nCho'tka maydonini tozalaydi."),
        _("actor.colliderect(obyekt) -> bool \n\nRect-ga asoslanib ikkita Actor obyekti o'rtasida to'qnashuv mavjudligini tekshiradi."),
        _("actor.collide_pixel(obyekt) -> (Tuple[int, int] | None) \n\nRang bor pixel-ga asoslanib ikkita Actor obyekti o'rtasida to'qnashuv mavjudligini tekshiradi."),
        _("actor.collidepoint_pixel((x, y joylashuvi)) -> int \n\nBerilgan x, y-joylashuviga asoslanib Actor obyekti bilan to'qnashuv mavjudligini tekshiradi."),
        _("game.exit() \n\nDasturni tamomlaydi."),
        _("sounds.play([ijro etish soni=Shart emas]) \n\nOvozni sozilangan marta ijro etadi. Agar sozlamasa, faqat bir marta ijro etadi."),
        _("pygame.display.update([Rect=Shart emas]) \n\nSozilgangan Rect hududdagi ekranni yangilaydi.\nAgar Rect sozilanmagan boʻlsa, butun ekran yangilanadi."),
    ]
}