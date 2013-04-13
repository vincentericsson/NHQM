float2 V(float2 r, float j)
{
    float V0=-70.0, Vso=-7.5, r0=2.0, d=0.65, l=1.0;
    float2 f=c_div(1.0f,c_add(1.0f,c_exp( c_div(c_sub(r,r0),d))));
    // float f=    1   /     (1   +  exp(            (r-r0)/d));
    float spin_orbit=0.5*(j*(j+1)-l*(l+1)-0.75);
    return c_mul(f,to_r(V0)-4*spin_orbit*c_div(f-to_r(1.0f),c_mul(to_r(d),r)));
    // return f*(V0-4*Vso*spin_orbit*(f-1)/(d*r));
}