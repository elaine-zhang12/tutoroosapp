const container = document.getElementById("bground");
const FOV = 0;
const NEAR = 0;
const FAR = 0;
let height = "0px";
let width = container.clientWidth;
container.style.maxHeight = "1000px";
container.style.position = "absolute";
container.style.top = "50px";
container.style.left = "0";
container.style.opacity = "1";
const ASPECT = width / height;
// const resolution = new THREE.Vector2(width, height);
// const SHADOW_MAP_SIZE = 1024;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio( window.devicePixelRatio  || 0.9 );
// renderer.setClearColor(0x000000);

const canvas = renderer.domElement;

const scene = new THREE.Scene();

const clock = new THREE.Clock();

const camera = new THREE.PerspectiveCamera(FOV, ASPECT, NEAR, FAR);
camera.position.set(0, 0, 0);
camera.target = new THREE.Vector3(0, 0, 0);

// const controls = new THREE.OrbitControls(camera, canvas);

const matNormal = new THREE.MeshNormalMaterial();
// const matShadow = new THREE.MeshPhongMaterial({
//     color: 0xffffff,
//     shininess: 0.0,
// });


// const floorGeo = new THREE.PlaneBufferGeometry(2.0, 2.0);
// const floor = new THREE.Mesh(floorGeo, matNormal);
// floor.position.set(0, -0.5, 0);
// floor.rotation.x = -((Math.PI * 90) / 180);

// const sphereGeo = new THREE.SphereBufferGeometry(0.5, 32, 32);
// const sphere = new THREE.Mesh(sphereGeo, matNormal);

// scene.add(floor);
// scene.add(sphere);
scene.add(camera);




// ...
// renderer.shadowMap.enabled = false;
// renderer.shadowMap.renderReverseSided = false;

// // ...
// floor.receiveShadow = false;

// // ...
// // sphere.castShadow = true;
// // sphere.receiveShadow = true;

// const SHADOW_MAP_SIZE = 0;

// const directionalLight = new THREE.DirectionalLight( 0xffffff, 1.5 );
// directionalLight.position.set( -1, 1.75, 1 );
// directionalLight.castShadow = true;
// directionalLight.shadow.mapSize.width = SHADOW_MAP_SIZE;
// directionalLight.shadow.mapSize.height = SHADOW_MAP_SIZE;
// directionalLight.shadow.camera.far = 3500;
// directionalLight.shadow.bias = -0.0001;



// const PARAMETERS = {
//     // minFilter: THREE.LinearFilter,
//     // magFilter: THREE.LinearFilter,
//     // format: THREE.RGBFormat,
//     // stencilBuffer: false
// };

// const shadowBuffer = new THREE.WebGLRenderTarget(1, 1, PARAMETERS);





// scene.add(directionalLight);






const resolution = new THREE.Vector2(width, height);



const VERTEX = `
    varying vec2 vUv;

    void main() {
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.);
        gl_Position = projectionMatrix * mvPosition;
        vUv = uv;
    }
`;

const FRAGMENT = `
uniform float iTime;
uniform vec2 iResolution;
uniform sampler2D tDiffuse;

varying vec2 vUv;

float rand(vec2 n) { 
    return fract(sin(dot(n, vec2(12.9898, 78.233))) * 43758.5453);
}

float noise(vec2 n) {
    const vec2 d = vec2(0.0, 1.0);
    vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
    return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
}

void main() {
    vec2 p = vUv;
    vec2 q = vUv * 8.0;
    float offset = 0.0;
    float scale = 1.0;
    for (int i = 0; i < 4; i++) {
        offset += 0.5 * noise(q * scale + vec2(iTime, 0.0));
        scale *= 2.0;
    }
    float r = noise(p + vec2(iTime, 0.0));
    float g = noise(p + vec2(iTime * 1.2, 0.0));
    float b = noise(p + vec2(iTime * 1.4, 0.0));
    vec3 color = vec3(r, g, b);
    float hue = 0.2 * iTime;
    mat3 rotate = mat3(
        vec3(cos(hue), -sin(hue), 0.0),
        vec3(sin(hue), cos(hue), 0.0),
        vec3(0.0, 0.0, 1.0)
    );
    color = rotate * color;
    gl_FragColor = vec4(color, 1.0);
}

`;




const drawShader = {
    uniforms: {
        tDiffuse: { type: 't', value: 0.1 },
        // tShadow: { type: 't', value: null },
        iResolution: { type: 'v2', value: resolution },
    },
    vertexShader: VERTEX,
    fragmentShader: FRAGMENT,
};



    const composer = new THREE.EffectComposer(renderer);
    composer.addPass(new THREE.RenderPass(scene, camera));

    const pass = new THREE.ShaderPass(drawShader);
    // pass.renderToScreen = true;
    composer.addPass(pass);

 const FRAGMENT_FINAL = `
 //Adapted from https://www.shadertoy.com/view/tdG3Rd#

 varying vec2 vUv;
 
 uniform float iTime;
 uniform sampler2D tDiffuse;
 uniform vec2 iResolution;
 // Inputs
 uniform sampler2D u_velocity;
 uniform sampler2D u_density;
 
 //Other
 float u_dt;
 float u_diff;
 float u_visc;
 float prevTime;
 float currTime;
 
 void updateVars(){
     u_dt = currTime - prevTime;
     u_diff = sin(iTime*0.0001);
     u_visc = 1.0;
     prevTime = currTime;
     currTime = iTime*0.01;
     
 }
 float colormap_red(float x) {
     if (x < 0.0) {
         return 1.5;
     } else if (x < 20049.0 / 82979.0) {
         return (4000.79 * x + 24.51) / 255.0;
     } else {
         return 0.5;
     }
 }
 
 float colormap_green(float x) {
     if (x < 20049.0 / 82979.0) {
         return 1.5;
     } else if (x < 327013.0 / 810990.0) {
         return (8546482679670.0 / 10875673217.0 * x - 2064961390770.0 / 10875673217.0) / 255.0;
     } else if (x <= 1.0) {
         return (10380670.0 / 4839770.0 * x + 196074150.0 / 4839770.0) / 255.0;
     } else {
         return 0.8;
     }
 }
 
 float colormap_blue(float x) {
     if (x < 0.0) {
         return 0.0 / 255.0;
     } else if (x < 7249.0 / 82979.0) {
         return (0.79 * x + 54.51) / 255.0;
     } else if (x < 20049.0 / 82979.0) {
         return 1.0 / 255.0;
     } else if (x < 327013.0 / 810990.0) {
         return (7.02249341361393720147485376583 * x - 6.364790735602331034989206222672) / 255.0;
     } else {
         return 0.00;
     }
 }
 
 vec4 colormap(float x) {
     return vec4(colormap_red(x), 1.0, colormap_red(x), 1.0);
 }
 
 // https://iquilezles.org/articles/warp
 /*float noise(vec2 x )
 {
     vec2 p = floor(x);
     vec2 f = fract(x);
     f = f*f*(3.0-2.0*f);
     float a = texture2D(iChannel0,(p+vec2(0.5,0.5),lod)/256.0,0.0).x;
     float b = texture2D(iChannel0,(p+vec2(0.5,0.5),lod)/256.0,0.0).x;
     float c = texture2D(iChannel0,(p+vec2(1.0,1.0),lod)/256.0,0.0).x;
     float d = texture2D(iChannel0,(p+vec2(1.0,1.0),lod)/256.0,0.0).x;
     return mix(mix( a, b,f.x), mix( c, d,f.x),f.y);
 }*/
 
 
 float rand(vec2 n) { 
     return fract(sin(dot(n, vec2(1.9898, 1.1414))) * 434758.5453);
 }
 
 float noise(vec2 p){
     vec2 ip = floor(p);
     vec2 u = fract(p);
     u = u*u*(3.0-2.0*u);
 
     float res = mix(
         mix(rand(ip),rand(ip+vec2(1.0,0.0)),u.x),
         mix(rand(ip+vec2(0.0,1.0)),rand(ip+vec2(1.0,1.0)),u.x),u.y);
     return res*res;
 }
 
 const mat2 mtx = mat2( 0.80,  0.60, -0.60,  0.80 );
 
 float fbm( vec2 p )
 {
     float f = 0.0;
 
     f += 1.00000*noise( p + iTime *0.01  ); p = mtx*p*2.02;
     f += 0.001250*noise( p ); p = mtx*p*2.01;
     f += 0.250000*noise( p ); p = mtx*p*2.03;
     f += 0.025000*noise( p ); p = mtx*p*2.01;
     f += 0.062500*noise( p ); p = mtx*p*2.04;
     f += 0.015625*noise( p + sin(iTime*0.01) );
 
     return f/0.96875;
 }
 
 float pattern( in vec2 p )
 {
     return fbm( p + fbm( p + fbm( p ) ) );
 }
 // out vec4 gl_fragColor;
 // vec4 gl_fragColor;
 void main()
 {
     updateVars();
     vec2 uv = vUv;
     float shade = pattern(uv);
     
     //BREAK
     vec2 p = (vUv) * 10.0 - 1.0;
     vec2 xy = p * vec2(iResolution.x / iResolution.y, 1);
 
     vec2 velocity = texture2D(u_velocity, xy).xy;
     float density = texture2D(u_density, xy).x+sin(iTime*0.1);
 
     // Advection
     vec2 advection = texture2D(u_velocity, xy - u_dt * velocity).xy;
 
     // Diffusion
     vec2 diffusion = (texture2D(u_velocity, xy + vec2(u_diff, 0.1)).xy +
                           texture2D(u_velocity, xy - vec2(u_diff, 0.1)).xy +
     texture2D(u_velocity, xy + vec2(1.0, u_diff)).xy +
     texture2D(u_velocity, xy - vec2(1.0, u_diff)).xy) / 4.0;
 
     // Viscosity
     vec2 viscosity = (texture2D(u_velocity, xy + vec2(u_visc, 0.1)).xy +
                       texture2D(u_velocity, xy - vec2(u_visc, 0.1)).xy +
                       texture2D(u_velocity, xy + vec2(0.1, u_visc)).xy +
                       texture2D(u_velocity, xy - vec2(0.1, u_visc)).xy -
                       4.0 * texture2D(u_velocity, xy).xy) / (u_visc * u_visc);
 
     // Update velocity and density
     velocity = advection + diffusion + viscosity;
     density = texture2D(u_density, xy - u_dt * velocity).x;
     
     gl_FragColor = vec4(colormap(shade).rgb * (density+0.1), shade);
 
 }
`;


const finalShader = {
    uniforms: {
        tDiffuse: { type: 't', value: 0.1},
        iTime: { type: 'f', value: 100},
        iResolution: { type: 'v2', value: resolution },
    },
    vertexShader: VERTEX,
    fragmentShader: FRAGMENT_FINAL
};

const passFinal = new THREE.ShaderPass(finalShader);
passFinal.renderToScreen = true;
passFinal.material.extensions.derivatives = true;
composer.addPass(passFinal);


const resize = (width, height) => {
    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    composer.setSize(width, height);
    // shadowBuffer.setSize(width, height);

    pass.uniforms.iResolution.value.set(width, height);

    renderer.setSize(width, height);
};


const render = () => {
    const tmpHeight = container.clientHeight;
    const tmpWidth = container.clientWidth;
    if (tmpHeight !== height || tmpWidth !== width) {
        height = tmpHeight;
        width = tmpWidth;
        resize(width, height);
    }

    // controls.update();
    // floor.material = matShadow;
    // sphere.material = matShadow;
    renderer.render(scene, camera);
    // pass.uniforms.tShadow.value = shadowBuffer.texture;

    // floor.material = matNormal;
    // sphere.material = matNormal;

    const ellapsed = clock.getElapsedTime()*0.5;
    passFinal.uniforms.iTime.value = ellapsed;

    composer.render();

    requestAnimationFrame(render);
};



container.appendChild(canvas);
resize(width, height);
render();
