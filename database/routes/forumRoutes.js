const express = require('express');
const router = express.Router();
const db = require('../db');

// Get members
router.get('/courses/:courseId/members', (req, res) => {
    const { courseId } = req.params;
    db.query(
        `SELECT u.user_id, u.username, e.role
         FROM enrollments e
         JOIN users u ON e.user_id = u.user_id
         WHERE e.course_id = ?`,
        [courseId],
        (err, results) => {
            if (err) return res.status(500).json(err);
            res.json(results);
        }
    );
});

// Get forums
router.get('/courses/:courseId/forums', (req, res) => {
    const { courseId } = req.params;
    db.query(
        'SELECT * FROM forums WHERE course_id = ?',
        [courseId],
        (err, results) => {
            if (err) return res.status(500).json(err);
            res.json(results);
        }
    );
});

// Create forum
router.post('/courses/:courseId/forums', (req, res) => {
    const { courseId } = req.params;
    const { title, user_id } = req.body;

    db.query(
        'INSERT INTO forums (course_id, title, created_by) VALUES (?, ?, ?)',
        [courseId, title, user_id],
        (err, result) => {
            if (err) return res.status(500).json(err);
            res.json({ message: 'Forum created' });
        }
    );
});

module.exports = router;