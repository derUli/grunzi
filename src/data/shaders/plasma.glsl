float hash(in vec2 uv){
    return fract(sin(dot(uv, vec2(14.478473612, 53.252567))) * 37482.1);
}

vec2 hash2(in vec2 uv)
{
    vec3 o = fract(vec3(uv.yxx*893.335)*vec3(0.146651, 0.185677, 0.135812));
    o += dot(o.zxy, o.yzx+60.424);
    return fract((o.yx+o.zy)*o.xz);
}

float voronoi (in vec2 uv, in float zPos, in float seed, in float blend)
{
    float build = 0.;
    float dist = 0.;
    for (float x = -2.; x <= 2.; x++)
    {
        for (float y = -2.; y <= 2.; y++)
        {
            vec2 cell = vec2(x,y);
            vec2 ID = floor(uv)-cell+seed;
            float rand = (zPos+hash(ID))*(hash(ID)*0.5+0.5);
            float B = fract(rand);
            vec3 offs = vec3(floor(rand),ceil(rand),B*B*(3.-2.*B));
            vec2 point = mix(hash2(ID+offs.x),hash2(ID+offs.y),offs.z);

            float distP = distance(point,fract(uv)+cell)-2.;
            build = mix(distP,build,smoothstep(build-blend,build+blend,distP));
        }
    }
    return build+2.;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = (fragCoord-.5*iResolution.xy)/iResolution.y;

    float scale = 0.7;
    float rescale = 1.3;
    float scalebright = 0.4;
    float m = 0., s = 0., h = 0., t = 0., cn = 0.;
    float vo1 = 0.;
    float vo2 = 0.;

    for (int i = 0; i < 8; i++) {
        m = float(i)/rescale+1.;
        s = float(i)*2.231+1.31354;
        h = 1./(float(i)/scalebright+1.);
        t = iTime*(float(i)/2.+1.)/4.;
        vo1 += voronoi((uv*m)/scale+hash2(vec2(float(i))+0.4443),t,s,0.)*h;
        vo2 += voronoi((uv*m)/scale+hash2(vec2(float(i))+0.4443),t,s+0.4123,0.)*h;
        cn += h;
    }

    vec3 col = vec3(vo1/cn) * vec3(1.0,0.5,0.0);
    col += vec3(vo2/cn) * vec3(0.0,0.5,1.0);
    col = clamp(pow(col,vec3(3.))*3.,0.,1.);

    fragColor = vec4(col,1.0);
}