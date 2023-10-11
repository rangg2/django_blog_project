// 공유버튼 클릭시에 클립보드로 복사하는 자바스크립트 코드
    // 공유하기 버튼 클릭 시
    document.querySelector('.share-button').addEventListener('click', async function() {
        let postUrl = window.location.href;
        
        try {
          await navigator.clipboard.writeText(postUrl);
          alert('포스트 링크가 클립보드에 복사되었습니다');
        } catch (err) {
          console.error('클립보드 복사 실패:', err);
        }
      });
