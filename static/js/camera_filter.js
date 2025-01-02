const cameraFeed = document.getElementById('camera-feed');
const overlayImg = document.getElementById('overlay-img');
const designItems = document.querySelectorAll('.design-item');
const cameraContainer = document.getElementById('camera-container');

let offsetX = 0;
let offsetY = 0;

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
        cameraFeed.srcObject = stream;
    } catch (err) {
        console.error("Error accessing camera:", err);
    }
}

function enableGestures() {
    const hammer = new Hammer(overlayImg);

    hammer.add(new Hammer.Pan({ direction: Hammer.DIRECTION_ALL, threshold: 0 }));
    hammer.on("pan", (e) => {
        let newLeft = offsetX + e.deltaX;
        let newTop = offsetY + e.deltaY;

        newLeft = Math.max(0, Math.min(cameraContainer.clientWidth - overlayImg.clientWidth, newLeft));
        newTop = Math.max(0, Math.min(cameraContainer.clientHeight - overlayImg.clientHeight, newTop));

        overlayImg.style.left = `${newLeft}px`;
        overlayImg.style.top = `${newTop}px`;
    });

    hammer.add(new Hammer.Pinch());
    hammer.on("pinch", (e) => {
        const scale = Math.min(Math.max(0.5, e.scale), 3); 
        overlayImg.style.transform = `scale(${scale})`;
    });

    overlayImg.addEventListener('panend', (e) => {
        offsetX += e.deltaX; 
        offsetY += e.deltaY;

        
        offsetX = Math.max(0, Math.min(cameraContainer.clientWidth - overlayImg.clientWidth, offsetX));
        offsetY = Math.max(0, Math.min(cameraContainer.clientHeight - overlayImg.clientHeight, offsetY));
    });
}


designItems.forEach(item => {
    item.addEventListener('click', () => {
        const designSrc = item.getAttribute('data-src');
        overlayImg.src = designSrc;
        overlayImg.style.display = 'block';
        overlayImg.style.position = 'absolute';
        overlayImg.style.left = '0px';
        overlayImg.style.top = '0px';
        overlayImg.style.transform = 'scale(1)';

        offsetX = 0; 
        offsetY = 0;

        enableGestures();
    });
});

startCamera();
