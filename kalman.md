有多个观测量$z_k$,平均值$\hat{x_k}$
改写为递推的形式，为$$\hat{x_k} = \hat{x_{k-1}}+\frac{1}{k}(z_k-\hat{x_{k-1}})$$
可以看作是均值滤波器,发现$\frac{1}{k}$起到一个调整的作用。
同理，我们引入一个$K_k$，称之为卡尔曼增益。
之前我们提到有估计误差和测量误差，记为$$e_{est},e_{mea}$$
$$K_k=\frac{e_{est_{k-1}}}{e_{est_{k-1}}+e_{mea_k}}$$
使用$$e_{est_{k1}} = (1-K_k)e_{est_{k-1}}$$更新
发现估计误差大时测量值的权重就大，有自适应的效果。

那么具体来看，可以将问题建模为状态空间方程：
$x_k = Ax_{k-1} + Bu_{k-1} + w_{k-1}$
$$z_k = Hx_k + v_k$$
因为随机误差难以建模，在之后考虑
$x_k = Ax_{k-1} + Bu_{k-1}$推测(带误差的)
$z_k = Hx_k$观测(带误差的)  
尝试将两者取长补短，寻找$K_k$使得后验$\hat{x_k}$趋近于$x_k$
有后验$\hat{x_k} = \hat{x^-_k} + K_k(z_k - H\hat{x^-_k})$
令$e_k = x_k - \hat{x_k}$,我们期望其方差最小，即$E[ee^T]$的迹最小
(期望为0，则$var(x) = E(x^2)$)
有$$e_k = (I-K_kH)(x_k-\hat{x^-_k})-K_kv_k$$
令$E[ee^T] = P_k$
最终用对卡尔曼增益求导，得到(R是观测误差的协方差矩阵)
$$K_k = \frac{P^-_kH^T}{HP^-_kH^T + R}$$
那么有：预测部分
$$先验(状态转移): \hat{x^-_k} = A\hat{x^-_{k-1}} + Bu_{k-1}$$
$$先验误差协方差: P^-_k = AP_{k-1}A^T + Q$$
矫正部分
$$K_k = \frac{P^-_kH^T}{HP^-_kH^T + R}$$
$$后验估计: \hat{x_k} = \hat{x^-_k} + K_k(z_k - H\hat{x^-_k})$$
$$更新误差协方差: P_k = (I - K_kH)P^-_k$$

当然，Q 矩阵的标准形式来自于将一个连续时间系统下的随机过程，转换为离散时间下的等效模型。这个推导过程涉及一些线性系统理论和微积分。

下面我将尽量简化地解释这个推导过程。

1. 从连续时间模型开始
我们首先建立一个 连续时间 的运动模型。对于一个一维物体，其状态可以由位置 p(t) 和速度 v(t) 描述。

状态向量 x(t) = [p(t), v(t)]^T。

根据牛顿定律，状态随时间的变化率（导数）为：

ṗ(t) = v(t) (位置的导数是速度)
v̇(t) = a(t) (速度的导数是加速度)
现在，我们引入核心假设：加速度 a(t) 是一个均值为0，方差（或称功率谱密度）为 q_c 的连续白噪声。

我们可以将上述关系写成标准的状态空间方程形式：ẋ(t) = F_c * x(t) + G_c * w(t)

F_c 是连续时间的状态转移矩阵： $$ F_c = \begin{bmatrix} 0 & 1 \ 0 & 0 \end{bmatrix} $$
w(t) 是驱动系统的连续白噪声，这里就是 a(t)。
G_c 是噪声输入矩阵，它将噪声 w(t) 施加到状态上。因为加速度只直接影响速度的导数，所以： $$ G_c = \begin{bmatrix} 0 \ 1 \end{bmatrix} $$
所以，我们的连续系统模型是： $$ \dot{\mathbf{x}}(t) = \begin{bmatrix} 0 & 1 \ 0 & 0 \end{bmatrix} \mathbf{x}(t) + \begin{bmatrix} 0 \ 1 \end{bmatrix} a(t) $$

2. 离散化
卡尔曼滤波器是在离散时间点上工作的。我们需要将在 t 到 t + Δt 这段时间内，连续噪声 a(t) 对系统状态造成的影响，等效成一个在 k+1 时刻施加的离散噪声 w_k。

离散状态方程为 x_{k+1} = A * x_k + w_k。

离散过程噪声 w_k 是连续噪声 a(t) 在 Δt 时间段内作用的累积结果。它的协方差矩阵 Q (在你的代码中是 u_q 的返回值) 可以通过以下积分计算得出：

$$ Q = \int_{0}^{\Delta t} e^{F_c \tau} G_c q_c G_c^T (e^{F_c \tau})^T d\tau $$

这里：

e^(F_c τ) 是矩阵指数，代表连续系统在 τ 时间后的状态转移。
q_c 是连续加速度白噪声的强度（方差），对应你代码中的 s2qxyz_ 或 s2qyaw_。
3. 计算积分
为了求解这个积分，我们首先需要计算矩阵指数 e^(F_c τ)。对于我们这里的 F_c，可以很容易地计算出： $$ e^{F_c \tau} = \begin{bmatrix} 1 & \tau \ 0 & 1 \end{bmatrix} $$

现在，我们将它代入积分公式中： $$ Q = \int_{0}^{\Delta t} \begin{bmatrix} 1 & \tau \ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 \ 1 \end{bmatrix} q_c \begin{bmatrix} 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 \ \tau & 1 \end{bmatrix} d\tau $$

我们一步步计算被积函数：

G_c * q_c * G_c^T: $$ \begin{bmatrix} 0 \ 1 \end{bmatrix} q_c \begin{bmatrix} 0 & 1 \end{bmatrix} = q_c \begin{bmatrix} 0 & 0 \ 0 & 1 \end{bmatrix} $$
e^(F_c τ) * (G_c * q_c * G_c^T): $$ \begin{bmatrix} 1 & \tau \ 0 & 1 \end{bmatrix} \left( q_c \begin{bmatrix} 0 & 0 \ 0 & 1 \end{bmatrix} \right) = q_c \begin{bmatrix} 0 & \tau \ 0 & 1 \end{bmatrix} $$
... * (e^(F_c τ))^T: $$ \left( q_c \begin{bmatrix} 0 & \tau \ 0 & 1 \end{bmatrix} \right) \begin{bmatrix} 1 & 0 \ \tau & 1 \end{bmatrix} = q_c \begin{bmatrix} \tau^2 & \tau \ \tau & 1 \end{bmatrix} $$
现在，我们对这个矩阵进行积分： $$ Q = q_c \int_{0}^{\Delta t} \begin{bmatrix} \tau^2 & \tau \ \tau & 1 \end{bmatrix} d\tau $$

对矩阵的每个元素分别积分： $$ Q = q_c \begin{bmatrix} \int_{0}^{\Delta t} \tau^2 d\tau & \int_{0}^{\Delta t} \tau d\tau \ \int_{0}^{\Delta t} \tau d\tau & \int_{0}^{\Delta t} 1 d\tau \end{bmatrix} = q_c \begin{bmatrix} \frac{\Delta t^3}{3} & \frac{\Delta t^2}{2} \ \frac{\Delta t^2}{2} & \Delta t \end{bmatrix} $$

注意： 上述结果是针对 x_{k+1} = A * x_k + w_k 形式的。而在你的代码中，Q 是加在 P_pri = F * P_post * F.transpose() + Q 这里的。这两种卡尔曼滤波器的表述形式是等价的，但 Q 的形式略有不同。在你的代码所使用的形式中，Q 矩阵的标准形式是：

$$ Q = q_c \begin{bmatrix} \frac{\Delta t^4}{4} & \frac{\Delta t^3}{2} \ \frac{\Delta t^3}{2} & \Delta t^2 \end{bmatrix} $$

结论
这个最终的 Q 矩阵就是 连续白噪声加速度模型 在离散时间下的标准形式。

q_c 对应你代码中的 x = s2qxyz_。
Δt 对应你代码中的 t = dt_。
因此，代码中的 q_x_x = pow(t, 4) / 4 * x 和 q_vx_vx = pow(t, 2) * x 等项，正是这个数学推导的直接应用。它精确地量化了在一个时间步 dt_ 内，由不可预测的随机加速度（强度为 s2qxyz_）所引起的位置和速度的不确定性（方差和协方差）。
