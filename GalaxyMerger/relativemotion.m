%% Relative Motion
function dydt = relativemotion(t,f)
% t is the time in seconds
% f is the position and velocity vector combined
% ex/ [Rx Ry Rz Vx Vy Vz]

% use ode45(@relativemotion,t,f,options)to find the position
% and velocity vectors of a spacecraft in orbit with the initial
% position and velocity vectors after a period of time
% Assumption: No Pertubations

mu = 398600;
x = f(1);
y = f(2);
z = f(3);
vx = f(4);
vy = f(5);
vz = f(6);

r = norm([x y z]);

ax = -(mu/(r^3))*x;
ay = -(mu/(r^3))*y;
az = -(mu/(r^3))*z;

dydt = [vx vy vz ax ay az]';
end