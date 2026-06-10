"""
WooaVideo KO 페이지 메타 디스크립션 CTR 최적화
- 기준: 네이버 서치어드바이저 노출 대비 CTR 개선
- 최우선: "동영상 자르기 무료" 25+9+2+1+1 = 38 노출 합계, 0% CTR → video-cut.html
- 전략: 키워드 선행 + "즉시·무설치·무료" 강조, 수동형("하세요") → 능동형 수치 표현
"""
import re, os

BASE = 'C:/개인/wooahouse/wooavideo'

# { 파일: (설명매칭prefix, 새_description) }
PAGES = {
    'index.html': (
        '동영상 압축·변환·자르기·크롭·워터마크',
        '동영상 자르기·압축·변환·크롭·회전·워터마크 등 무설치 무료 온라인 동영상 편집 도구 모음. 회원가입 없이 브라우저에서 바로 사용, 파일은 서버에 저장되지 않아 100% 안전 — 우아비디오(WooaVideo)'
    ),
    # ── 38 노출 0% CTR: 최우선 ─────────────────────────────────────────
    'video-cut.html': (
        '동영상의 원하는 구간을 설치 없이',
        '동영상 자르기 무료 — 원하는 구간을 클릭 몇 번으로 즉시 추출. MP4·MOV·AVI 지원, 회원가입·설치 없이 브라우저에서 바로 사용. 파일은 서버로 전송되지 않아 100% 안전.'
    ),
    # ── mp4 용량 줄이기 관련 ───────────────────────────────────────────
    'video-compress.html': (
        'MP4·MOV·AVI 동영상을 설치 없이 브라우저에서 무료로 압축',
        '동영상 압축 무료 — MP4·MOV·AVI 용량을 무설치로 즉시 줄이기. 화질 손실 최소화, 이메일·카카오톡 첨부 가능한 크기로 압축. 회원가입·설치 없이 브라우저에서 바로 사용.'
    ),
    # ── 무료 동영상 변환 ──────────────────────────────────────────────
    'video-convert.html': (
        'MP4·AVI·MOV·WebM·MKV 동영상 포맷을 설치 없이',
        '동영상 포맷 변환 무료 — MP4·AVI·MOV·WebM·MKV를 무설치로 즉시 변환. 회원가입 없이 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    # ── 나머지 전체 ────────────────────────────────────────────────────
    'video-crop.html': (
        '동영상을 16:9·9:16·1:1 등 원하는 비율로 크롭',
        '동영상 크롭 무료 — 16:9·9:16·1:1 등 원하는 비율로 즉시 잘라내기. 유튜브·릴스·인스타그램 규격으로 무설치 변환, 회원가입 없이 바로 사용.'
    ),
    'video-merge.html': (
        '여러 동영상 파일을 하나로 이어 붙이세요',
        '동영상 합치기 무료 — 여러 영상을 하나로 이어 붙이기, 무설치로 즉시 사용. 회원가입 없이 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-rotate.html': (
        '동영상을 90°·180°·270° 회전하거나',
        '동영상 회전·뒤집기 무료 — 90°·180°·270° 회전, 좌우·상하 반전을 즉시 적용. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-speed.html': (
        '동영상을 0.25배속~4배속으로',
        '동영상 속도 조절 무료 — 0.25배~4배속으로 빠르게·느리게 즉시 변경. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-watermark.html': (
        '동영상에 텍스트 워터마크를 설치 없이',
        '동영상 워터마크 추가 무료 — 텍스트 로고를 동영상에 삽입, 위치·크기·색상·투명도 자유 설정. 무설치로 브라우저에서 바로 사용, 회원가입 없이 즉시.'
    ),
    'video-mute.html': (
        '동영상에서 소리를 제거하여',
        '동영상 음소거 무료 — 동영상 소리를 제거해 무음으로 즉시 저장. 무설치로 브라우저에서 바로 사용, 회원가입 없이 즉시 가능.'
    ),
    'video-resize.html': (
        '동영상 해상도를 1080p·720p·480p',
        '동영상 해상도 변경 무료 — 1080p·720p·480p로 즉시 변경, mp4 용량 줄이기에도 효과적. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-to-mp3.html': (
        'MP4·MOV·AVI 동영상에서 MP3·AAC·WAV',
        '동영상 MP3 추출 무료 — MP4·MOV·AVI에서 MP3·AAC·WAV 음원을 즉시 추출. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-add-audio.html': (
        '동영상에 배경음악을 추가하거나',
        '동영상 배경음악 추가·교체 무료 — 동영상에 음악을 넣거나 기존 음성을 교체. 무설치로 브라우저에서 바로 사용, 회원가입 없이 즉시 가능.'
    ),
    'video-volume.html': (
        '동영상 소리를 설치 없이 브라우저에서 무료로',
        '동영상 볼륨 조절 무료 — 동영상 소리를 키우거나 줄이기를 즉시 적용. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'video-thumbnail.html': (
        '동영상의 원하는 시점 프레임을',
        '동영상 썸네일 추출 무료 — 원하는 시점 프레임을 이미지로 즉시 저장. 무설치로 브라우저에서 바로 사용, 회원가입 없이 즉시 가능.'
    ),
    'video-info.html': (
        '동영상 파일의 해상도·길이·파일 크기',
        '동영상 정보 확인 무료 — 해상도·재생시간·파일 크기·포맷·비트레이트를 즉시 확인. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
    'mp4-to-gif.html': (
        'MP4·MOV·AVI 동영상의 일부를 GIF로',
        'MP4를 GIF로 변환 무료 — 동영상의 원하는 구간을 GIF 애니메이션으로 즉시 변환. 시작 시간·길이·크기·FPS 조절 가능, 무설치로 브라우저에서 바로 사용.'
    ),
    'gif-to-mp4.html': (
        'GIF 애니메이션을 MP4 동영상으로',
        'GIF를 MP4로 변환 무료 — GIF 애니메이션을 MP4 동영상으로 즉시 변환. 무설치로 브라우저에서 바로 사용, 파일은 서버로 전송되지 않아 안전.'
    ),
}

ok_count = 0
fail_count = 0

for fname, (match_prefix, new_desc) in PAGES.items():
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        print(f'  SKIP (없음): {fname}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(<meta name="description" content=")[^"]*(")'

    def desc_replacer(m):
        if match_prefix in m.group(0):
            return m.group(1) + new_desc + m.group(2)
        return m.group(0)

    new_content = re.sub(pattern, desc_replacer, content)

    if new_content == content:
        print(f'  MISS: {fname} — "{match_prefix[:35]}"')
        fail_count += 1
        continue

    # og:description / twitter:description 동기화
    new_content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2),
        new_content
    )
    new_content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2),
        new_content
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  OK: {fname}')
    ok_count += 1

print(f'\n완료: {ok_count}개 교체, {fail_count}개 실패')
