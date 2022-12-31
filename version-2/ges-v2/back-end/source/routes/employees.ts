import express from 'express';
import controller from '../controllers/employees';

const router = express.Router();

router.get('/employees', controller.getEmployees);
router.post('/employees', controller.addEmployee);

router.get('/employee/:id', controller.getEmployee);
router.post('/employee/:id', controller.addException);
router.put('/employee/:id', controller.updateEmployee);
router.delete('/employee/:id', controller.deleteEmployee);

export default router;