float2 c_add(float2 a, float2 b) {return (float2)(a.x+b.x,a.y+b.y);}
float2 c_sub(float2 a, float2 b) {return (float2)(a.x-b.x,a.y-b.y);}
float2 c_mul(float2 a, float2 b) {return (float2)(a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x);}
float2 c_sin(float2 z) {return (float2)(sin(z.x)*cosh(z.y),cos(z.x)*sinh(z.y));}
float2 c_cos(float2 z) {return (float2)(cos(z.x)*cosh(z.y),sin(z.x)*sinh(z.y));}
float2 c_exp(float2 z) {return (float2)(exp(z.x)*cos(z.y),exp(z.x)*sin(z.y));}
float2 to_r(float x) {return (float2)(x,0.0f);}
float2 to_i(float y) {return (float2)(0.0f,y);}
float2 to_c(float x, float y) {return (float2)(x,y);}
bool eps_r(float2 z) {return z.x<0.0000000001;}
bool eps_i(float2 z) {return z.y<0.0000000001;}
bool eps_c(float2 z) {return eps_r(z)&&eps_i(z);}
float real(float2 z) {return z.x;}
float imag(float2 z) {return z.y;}
float2 epsify(float2 z)
{
    if (eps_r(z))
        z.x=0.0000000001;
    if (eps_i(z))
        z.y=0.0000000001;
    return z;
}
float2 c_div(float2 a, float2 b)
{
    float denominator=b.x*b.x+b.y*b.y;
    float2 factor=c_mul(a,(float2)(b.x,-b.y));
    return (float2)(factor.x/denominator,factor.y/denominator);
}
// float2 c_div(float a, float2 b) {return c_div((float2)(a,0.0f),b);}
// float2 c_div(float2 a, float b) {return c_div(a,(float2)(b,0.0f));}
// float2 c_mul(float a, float2 b) {return c_mul((float2)(a,0.0f),b);}
// float2 c_mul(float2 a, float b) {return c_mul(b,a);}
// float2 c_add(float a, float2 b) {return c_add((float2)(a,0.0f),b);}
// float2 c_add(float2 a, float b) {return c_add(b,a);}
// float2 c_sub(float a, float2 b) {return c_sub((float2)(a,0.0f),b);}
// float2 c_sub(float2 a, float b) {return c_sub(a,(float2)(b,0.0f));}