window.addEventListener("DOMContentLoaded", init);

function init() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const renderer = new THREE.WebGLRenderer({
        canvas: document.querySelector("#mainCanvas")
    });
    
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(width, height);

    const camera = new THREE.PerspectiveCamera(
        45,
        width / height,
        1,
        10000
    );

    const scene = new THREE.Scene();

    camera.position.set(0, 0, +1000);

    const geometry = new THREE.BoxGeometry(100, 100, 100);
    const material = new THREE.MeshStandardMaterial({
        color: 0x0000ff
    });
    const box = new THREE.Mesh(geometry, material);
    scene.add(box);

    const light_pos = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]

    const directionalLight1 = new THREE.DirectionalLight(
        0xffffff
    );
    directionalLight1.position.set(1, 1, 1);
    directionalLight1.intensity = 2;
    const directionalLight1 = new THREE.DirectionalLight(
        0xffffff
    );
    directionalLight1.position.set(1, 1, 1);
    scene.add(directionalLight);

    function tick() {
        requestAnimationFrame(tick);
    
        box.rotation.x += 0.01;
        box.rotation.y += 0.01;
    
        renderer.render(scene, camera);
    }
    
    tick();
}
