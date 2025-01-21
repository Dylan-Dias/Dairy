import React from 'react';
import styles from './Insights.module.css';

const Insights = () => {
  return (
    <div className={styles.dashboard}>
      <div className={styles.card}>
        <h2>Milk Yield</h2>
        <p>450 Liters Today</p>
      </div>
      <div className={styles.card}>
        <h2>Avg. Milking Time</h2>
        <p>15 mins</p>
      </div>
      <div className={styles.card}>
        <h2>Cows Milked</h2>
        <p>75 Cows</p>
      </div>

      <div className={styles.card}>
        <h2>Milking Schedule</h2>
        <p>Interactive calendar coming soon...</p>
      </div>

      <div className={styles.card}>
        <h2>Daily Insights</h2>
        <p>Date: 2025-01-01</p>
        <p>Milk Yield: 450 L</p>
        <p>Cows Milked: 75</p>
        <p>Avg. Time: 15 mins</p>
      </div>
      <div className={styles.card}>
        <h2>Daily Insights</h2>
        <p>Date: 2025-01-02</p>
        <p>Milk Yield: 480 L</p>
        <p>Cows Milked: 80</p>
        <p>Avg. Time: 14 mins</p>
      </div>
    </div>
  );
};

export default Insights;
