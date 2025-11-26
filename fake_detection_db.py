"""
MySQL helper for logging fake detection results.
Uses mysql-connector-python.
"""

from __future__ import annotations

import os
import threading
from typing import Optional

import mysql.connector


class FakeDetectionDB:
    """Simple MySQL helper to persist detection outcomes."""

    def __init__(self) -> None:
        self._config = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": int(os.getenv("MYSQL_PORT", "3306")),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", "root"),
            "database": os.getenv("MYSQL_DATABASE", "fake_detection_db"),
        }
        self._lock = threading.Lock()
        self._connect()
        self._ensure_table()

    def _connect(self) -> None:
        self._conn = mysql.connector.connect(**self._config)

    def _ensure_connection(self):
        try:
            self._conn.ping(reconnect=True, attempts=3, delay=2)
        except mysql.connector.Error:
            self._connect()
        return self._conn

    def _ensure_table(self) -> None:
        conn = self._ensure_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS detections (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    input_text TEXT NOT NULL,
                    prediction_label VARCHAR(20) NOT NULL,
                    detection_percent FLOAT NOT NULL,
                    detection_type VARCHAR(20) NOT NULL DEFAULT 'link',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
            conn.commit()
            try:
                cursor.execute(
                    "ALTER TABLE detections ADD COLUMN detection_type VARCHAR(20) NOT NULL DEFAULT 'link';"
                )
                conn.commit()
            except mysql.connector.Error:
                conn.rollback()
        finally:
            cursor.close()

    def insert_detection(
        self,
        input_text: str,
        prediction_label: str,
        detection_percent: float,
        detection_type: str = "link",
    ) -> None:
        """Insert a detection row into MySQL."""
        input_text = (input_text or "")[:4000]
        prediction_label = (prediction_label or "UNKNOWN")[:20]

        with self._lock:
            conn = self._ensure_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO detections (input_text, prediction_label, detection_percent, detection_type)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (input_text, prediction_label, float(detection_percent), detection_type),
                )
                conn.commit()
            finally:
                cursor.close()

    def fetch_by_filter(
        self,
        detection_type: str | None = None,
        prediction_label: str | None = None,
        limit: int = 200,
    ):
        """Fetch rows filtered by detection type and prediction label."""
        conditions = []
        params = []
        if detection_type:
            conditions.append("detection_type = %s")
            params.append(detection_type)
        if prediction_label:
            conditions.append("prediction_label = %s")
            params.append(prediction_label)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT id, input_text, prediction_label, detection_percent, detection_type, created_at
            FROM detections
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s
        """
        params.append(limit)

        with self._lock:
            conn = self._ensure_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()
            finally:
                cursor.close()
        return rows



