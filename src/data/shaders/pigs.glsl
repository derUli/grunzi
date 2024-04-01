vec2 rotate(in vec2 p, in float t)
{
	return p * cos(-t) + vec2(p.y, -p.x) * sin(-t);
}

float dePig(in vec3 p)
{
    p.y +=   0.3 * smoothstep( 0.2, 0.0, length(abs(p.zx) - vec2(0.4, 0.4))) * (1.0 - step(0.0, p.y));
    p.y +=  -0.2 * smoothstep(0.15, 0.0, length(abs(p.zx - vec2(0.4,0.0)) - vec2(0.0, 0.4))) * step(0.0, p.y);
    p.z += -0.15 * smoothstep( 0.4, 0.3, length(p.yx)) * step(0.0, p.z);
    p.z +=  0.15 * smoothstep( 0.1, 0.0, length(abs(p.yx) - vec2(0.0, 0.15))) * step(0.0, p.z);
    p.z +=   0.1 * smoothstep( 0.1, 0.0, length(abs(p.yx - vec2(0.4,0.0)) - vec2(0.0, 0.3))) * step(0.0, p.z);
    p.z +=  0.15 * smoothstep( 0.1, 0.0, length(p.yx - vec2(0.35,0.0))) * (1.0 - step(0.0, p.z));
    return 0.6 * (length(p) - 1.0);
}

float map1(in vec3 p)
{
    p.z -= iTime*2.0;
    p.xy = rotate(p.xy, p.z * 0.1);
    p.xy = rotate(p.xy, iTime * 0.2);
    p.z = mod(p.z, 4.0) - 2.0;
    p.xy = rotate(p.xy, iTime * 0.2);
    p.xy = abs(p.xy) - vec2(2.0);
    p.xy = rotate(p.xy, iTime * -0.5);
    return dePig(p);
}

float map2(in vec3 p)
{
 	return length(p - vec3(0.0, 0.0, -50.0)) - 20.0;
}

float map(in vec3 p)
{
    return min(map1(p), map2(p));
}

vec3 calcNormal(in vec3 p)
{
	const vec2 e = vec2(0.0001, 0.0);
	return normalize(vec3(
		map(p + e.xyy) - map(p - e.xyy),
		map(p + e.yxy) - map(p - e.yxy),
		map(p + e.yyx) - map(p - e.yyx)));
}

float march(in vec3 ro, in vec3 rd)
{
	const float maxd = 50.0;
	const float precis = 0.001;
    float h = precis * 2.0;
    float t = 0.0;
	float res = -1.0;
    for(int i = 0; i <256; i++)
    {
        if(h < precis || t > maxd) break;
	    h = map(ro + rd * t);
        t += h;
    }
    if(t < maxd) res = t;
    return res;
}

vec3 transform(in vec3 p)
{
    p.yz = rotate(p.yz, cos(iTime * 0.05)*0.3);
    p.zx = rotate(p.zx, sin(iTime * 0.1)*0.2);
    return p;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 p = (2.0 * fragCoord.xy - iResolution.xy) / iResolution.y;
	vec3 col = vec3(0.0,0.0,0.2)*(1.0+p.y);
   	vec3 rd = normalize(vec3(p, -1.8));
	vec3 ro = vec3(0.0, 0.0, 5.0);
    vec3 li = normalize(vec3(0.5, 0.8, 3.0));
    ro = transform(ro);
	rd = transform(rd);
    float t = march(ro, rd);
    if(t > -0.001)
    {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos);
		float dif = clamp((dot(n, li) + 0.5) * 0.7, 0.3, 1.0);
        float dep = exp(-0.001 * pos.z * pos.z);
        if (map1(pos) < map2(pos))
        {
            col = vec3(0.8, 0.5, 0.5) * dif * dep;
        } else {
            col = vec3(1.0, 0.9, 0.2) * dif * dif * dif;
        }
	}
   	fragColor = vec4(col, 1.0);
}
