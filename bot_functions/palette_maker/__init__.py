from .color_quantizer import ColorQuantizer

keywords = ['get-palette']

def make_palette(tweet, api):
    if tweet.in_reply_to_status_id is None:
        return
    text = tweet.text.lower()
    if not any(kw in text for kw in keywords):
        return

    mode = 'colorful'
    n_colors = 8

    word_list = text.split(' ')
    for word in word_list:
        if word.startswith('mode='):
            mode = word.split('=', 1)[1]
            if mode not in ('colorful', 'averaged'):
                mode = 'colorful'

        if word.startswith('numcolors='):
            try:
                n_colors = int(word.split('=', 1)[1])
                # print(n_colors)
            except ValueError:
                pass

    print(tweet.text)
    in_rep_to = api.get_status(tweet.in_reply_to_status_id)
    try:
        img_url = in_rep_to.entities['media'][0]['media_url']
        print(img_url)

        img = ColorQuantizer()
        img.open_from_url(img_url)
        if mode == 'colorful':
            img.nearest_color_quantize(limit=n_colors)
        elif mode == 'averaged':
            img.kmeans_quantize(n_clusters=n_colors)
        file_path = img.export_png()

        media = api.media_upload(file_path)
        api.update_status(
            status=f"@{tweet.user.screen_name} Extracted color palette:",
            media_ids=[media.media_id],
            in_reply_to_status_id=tweet.id,
        )
    except Exception as e:
        print(e)
        api.update_status(
            status=f"@{tweet.user.screen_name} No image was found",
            in_reply_to_status_id=tweet.id,
        )

    if not tweet.user.following:
        tweet.user.follow()

    return True