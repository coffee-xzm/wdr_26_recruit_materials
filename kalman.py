import numpy as np
import matplotlib.pyplot as plt

def kalman_filter(z, R, Q, A, H, P, x):

    x_prior = np.dot(A, x)
    P_prior = np.dot(np.dot(A, P), A.T) + Q
    K_numerator = np.dot(P_prior, H.T)
    K_denominator = np.dot(np.dot(H, P_prior), H.T) + R
    K = K_numerator / K_denominator
    
    # 基于测量值更新状态估计
    x_post = x_prior + K * (z - np.dot(H, x_prior))
    
    # 更新误差协方差
    P_post = np.dot((np.eye(P.shape[0]) - np.dot(K, H)), P_prior)
    
    return x_post, P_post

def main():
    # 时间步长
    dt = 1.0
    # 总时间步数
    num_steps = 100
    
    # --- 真实系统 ---
    # 真实位置和速度
    true_x = np.zeros(num_steps)
    true_v = np.zeros(num_steps)
    true_x[0] = 0.0
    true_v[0] = 1.0
    
    # 过程噪声的标准差 (模拟速度的微小变化)
    process_noise_std = 0.1
    
    for i in range(1, num_steps):
        true_v[i] = true_v[i-1] + np.random.normal(0, process_noise_std)
        true_x[i] = true_x[i-1] + true_v[i-1] * dt

    # --- 测量 ---
    # 测量噪声的标准差
    measurement_noise_std = 10.0
    # 带噪声的测量值 (只测量位置)
    measurements = true_x + np.random.normal(0, measurement_noise_std, num_steps)

    # --- 卡尔曼滤波器初始化 ---
    # 状态向量 [位置, 速度]'
    x = np.array([0.0, 0.0]) 
    
    # 状态转移矩阵 A
    A = np.array([[1, dt],
                  [0, 1]])
                  
    # 观测矩阵 H (只观测位置)
    H = np.array([1, 0])
    
    # 初始估计误差协方差 P
    P = np.array([[1000, 0],
                  [0, 1000]])
                  
    # 过程噪声协方差 Q
    # 基于随机加速度模型
    q_val = 0.1
    Q = q_val * np.array([[0.25*dt**4, 0.5*dt**3],
                         [0.5*dt**3, dt**2]])
                         
    # 测量噪声协方差 R
    R = measurement_noise_std**2
    
    # 用于存储卡尔曼滤波结果的列表
    kalman_estimates = []

    # --- 运行卡尔曼滤波器 ---
    for i in range(num_steps):
        z = measurements[i]
        x, P = kalman_filter(z, R, Q, A, H, P, x)
        kalman_estimates.append(x[0]) # 只存储位置估计

    # --- 绘图 ---
    plt.figure(figsize=(12, 8))
    plt.plot(range(num_steps), true_x, 'b-')
    plt.plot(range(num_steps), measurements, 'r.', markersize=4)
    plt.plot(range(num_steps), kalman_estimates, 'g-', linewidth=2)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()