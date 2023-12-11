import streamlit as st

def main():
    st.title("Streamlit HLS Video Player")

    # Replace 'your_hls_url_here' with the actual HLS URL you want to use
    # hls_url = "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3877970/1701868520_9313420424950984/1701868505553_509274441213191230_video_VOD.m3u8"
    # normal url 
    # hls_url = 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/original/1701868505553_509274441213191230_video_VOD.mp4'
    #  360p download url 
    hls_url = 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/download/3877970/1701868555_7736750338822450/1701868505553_509274441213191230_video_VOD360p30.mp4'
    start_time_seconds = 220.55

    if hls_url != "your_hls_url_here":
        # st.video(hls_url, format="video/mp4")
        st.video(hls_url,start_time=220)
        st.video(hls_url,start_time=220,format="video/m3u8")

        modified_video_url = f"{hls_url}#t={start_time_seconds}"

        st.video(modified_video_url)

if __name__ == "__main__":
    main()

    

    # "chrome-extension://eakdijdofmnclopcffkkgmndadhbjgka/player.html#https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3877970/1701868520_9313420424950984/1701868505553_509274441213191230_video_VOD.m3u8"



    # <iframe src=https://www.videocrypt.com/website/player_code?id=3878240_0_7982816139926658 title="VideoCrypt Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width:100%; height:calc(65vw*0.567)"></iframe>